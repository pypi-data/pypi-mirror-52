# -*- coding: utf-8 -*-

# shortrate
# ---------
# risk factor model library python style.
# 
# Author:   sonntagsgesicht, based on a fork of Deutsche Postbank [pbrisk]
# Version:  0.3, copyright Wednesday, 18 September 2019
# Website:  https://github.com/sonntagsgesicht/shortrate
# License:  Apache License 2.0 (see LICENSE file)


from businessdate import BusinessDate
from timewave import State, QuietConsumer, StochasticProcess, \
    GaussEvolutionFunctionProducer, CorrelatedGaussEvolutionProducer
from timewave.stochasticconsumer import _Statistics


class _OptionStatistics(_Statistics):
    _available = 'count', 'mean', 'stdev', 'variance', 'skewness', 'kurtosis', 'median', 'min', 'max', 'strike', 'put', 'call'

    def __init__(self, data, description='', strike=None, **expected):
        super(_OptionStatistics, self).__init__(data, description, **expected)
        put = (lambda s, k: sum(map((lambda x: max(k - x, 0)), s)) / float(len(s)))
        call = (lambda s, k: sum(map((lambda x: max(x - k, 0)), s)) / float(len(s)))
        self.strike = self.mean if strike is None else strike
        self.put = put(self.sample, self.strike)
        self.call = call(self.sample, self.strike)


class RiskFactor(object):
    """RiskFactor"""

    def __init__(self):
        super(RiskFactor, self).__init__()
        self._inner_factor = None
        self._factor_value = None
        self._factor_date = None

    @property
    def inner_factor(self):
        r"""
        RiskFactor typically move given data structure like yield curves, fx curves or volatility surfaces.
        The inner factor is the driven structure.
        """
        return self._inner_factor

    def pre_calculate(self, s, e):
        r"""
        :param BusinessDate s: start date pre calc step
        :param BusinessDate e: end date pre calc step

        pre calculation depending only on dates and model data
        """
        pass

    def set_risk_factor(self, factor_date, factor_value=None):
        r"""
        :param BusinessDate factor_date:
        :param float or tuple factor_value:

        sets risk factor state, method should be idempotent,
        i.e. setting same state twice must not change risk factor state at all
        """
        self._factor_value = factor_value
        self._factor_date = factor_date


class RiskFactorModel(StochasticProcess, RiskFactor):
    """RiskFactorModel which implements StochasticProcess evolve for timewave engine """

    @staticmethod
    def _default_day_count(start, end):
        if hasattr(start, 'diff_in_days'):
            # duck typing businessdate.BusinessDate.diff_in_days
            d = start.diff_in_days(end)
        else:
            d = end - start
            if hasattr(d, 'days'):
                # assume datetime.date or finance.BusinessDate (else days as float)
                d = d.days
        return float(d) / 365.25

    def __init__(self, inner_factor=None, start=0.0):
        r"""

        :param inner_factor: parameter object which is modeled by the risk factor model
        :type  inner_factor: Curve or Volatility or object
        :param start:
        :type  start: float or tuple

        initialize risk factor model
        """
        super(RiskFactorModel, self).__init__(start=start)
        # method: day_count, function to derive floats from dates and periods, i.e. year fractions
        self.day_count = self._default_day_count

        self._initial_factor_date = getattr(inner_factor, 'origin', BusinessDate())
        self._inner_factor = inner_factor

        self._factor_value = self.start
        self._factor_date = self._initial_factor_date

    def pre_calculate(self, s, e):
        r"""
        :param BusinessDate s: start date pre calc step
        :param BusinessDate e: end date pre calc step

        pre calculation depending only on dates and model data
        (RiskFactor method)
        """
        pass

    def get_numeraire(self, value_date):  # todo do I really need a value_date or isn't it given by _risk_fator date
        r"""
        :param BusinessDate value_date: date of
        :return float: returns the numeraire value
        """
        return self.start

    def evolve(self, x, s, e, q):
        r"""
        :param float x: current state value, i.e. value before evolution step
        :param BusinessDate s: current point in time, i.e. start point of next evolution step
        :param BusinessDate e: next point in time, i.e. end point of evolution step
        :param float q: standard normal random number to do step
        :return float: next state value, i.e. value after evolution step

        evolves process state `x` from `s` to `e` in time depending of standard normal random variable `q`
        """
        s = self.day_count(self._initial_factor_date, s)
        e = self.day_count(self._initial_factor_date, e)
        return super(RiskFactorModel, self).evolve(x, s, e, q)

    def evolve_risk_factor(self, x, s, e, q):
        r"""
        :param float x: current state value, i.e. value before evolution step
        :param BusinessDate s: current point in time, i.e. start point of next evolution step
        :param BusinessDate e: next point in time, i.e. end point of evolution step
        :param float q: standard normal random number to do step
        :return float: next state value, i.e. value after evolution step

        evolves process state `x` from `s` to `e` in time depending of standard normal random variable `q`
        and sets risk factor at `e` to `x` after evolving from `s`.
        """
        y = self.evolve(x, s, e, q)
        self.set_risk_factor(e, y)
        return y

    def set_risk_factor(self, factor_date=None, factor_value=None):
        r"""
        :param BusinessDate factor_date: sets risk factor state at this date
        :param factor_value: sets risk factor state to this value
        :type  factor_value: float or tuple

        sets risk factor state, method should be idempotent,
        i.e. setting same state twice must not change risk factor state at all
        (RiskFactor method)
        """
        self._factor_value = factor_value if factor_value else self.start
        self._factor_date = factor_date if factor_date else self._initial_factor_date


class RiskFactorState(State):
    """RiskFactorState"""

    def __init__(self, value=list(), numeraire_value=0.0):
        r"""
        :param list() value:
        :param float numeraire_value:

        inits RiskFactorState
        """
        super(RiskFactorState, self).__init__(value)
        # float: numeraire value in state
        self.numeraire = numeraire_value


class RiskFactorProducer(GaussEvolutionFunctionProducer):
    def __init__(self, process):
        r"""
        :param RiskFactorModel process:

        producer for `timewave` simulation framework to evolve a RiskFactorModel
        depending of standard normal random values
        """
        self.process = process
        self.diffusion_driver = process.diffusion_driver
        length = len(process) if len(process) > 1 else None
        super(RiskFactorProducer, self).__init__(process.evolve_risk_factor, State(process.start), length)

    def initialize(self, grid=None, num_of_paths=None, seed=None):
        r"""
        :param list(BusinessDate) grid: list of Monte Carlo grid dates
        :param int num_of_paths: number of simulation path
        :param hashable seed: initial seed of random generators

        sets pre calculation depending only on grid
        """
        super(RiskFactorProducer, self).initialize(grid, num_of_paths, seed)

        for s, e in zip(grid[:-1], grid[1:]):
            self.process.pre_calculate(s, e)

    def initialize_path(self, path_num=None):
        """initialize RiskFactorConsumer for path"""
        super(RiskFactorProducer, self).initialize_path(path_num)
        self.process.set_risk_factor(self.state.date)


class MultiRiskFactorProducer(CorrelatedGaussEvolutionProducer):

    def __init__(self, process_list, correlation=None, diffusion_driver=None):
        """
        :param list(RiskFactorModel) process_list:
        :param correlation: correlation of diffusion drivers of risk factors
        :type  correlation: list(list(float)) or dict((RiskFactorModel, RiskFactorModel): float)
        :param list(RiskFactorModel) diffusion_driver: index of diffusion driver
            if correlation is given by simple matrix (list(list(float)))

        initialize MultiRiskFactorProducer
        """
        producers = [RiskFactorProducer(p) for p in process_list]
        super(MultiRiskFactorProducer, self).__init__(producers, correlation, diffusion_driver)


class RiskFactorConsumer(QuietConsumer):
    """consumer of RiskFactorState"""

    def __init__(self, *risk_factor_list):
        """
        :param list(RiskFactor) risk_factor_list: list of risk factors which will be driven by risk factor state

        initialize RiskFactorConsumer
        """
        super(RiskFactorConsumer, self).__init__()
        if not len(set([c.origin for c in risk_factor_list])) == 1:
            raise AssertionError('Origin of risk factors must coincide. ')
        #: BusinessDate: valuation date
        self.start_date = risk_factor_list[0].origin
        self.initial_state = risk_factor_list

    def initialize(self, grid=None, num_of_paths=None, seed=None):
        r"""
        :param list(BusinessDate) grid: list of Monte Carlo grid dates
        :param int num_of_paths: number of simulation path
        :param hashable seed: initial seed of random generators

        sets pre calculation depending only on grid
        """
        super(RiskFactorConsumer, self).initialize(grid, num_of_paths, seed)

        for rf in self.initial_state:
            for s, e in zip(grid[:-1], grid[1:]):
                rf.pre_calculate(s, e)

    def initialize_path(self, path_num=None):
        """initialize RiskFactorConsumer for path"""
        for factor in self.state:
            factor.set_risk_factor(self.start_date)
        return self.state

    def consume(self, state):
        """
        :param RiskFactorState state: specific process state
        :return object: the new consumer state

        returns pair
        the first element is the list of updated simulated hw curves
        the second element is True (indicates Curve mapping)
        """
        for factor in self.state:
            factor.set_risk_factor(state.date, state.value)
        return self.state

    def finalize(self):
        """finalize RiskFactorConsumer"""
        for factor in self.initial_state:
            factor.set_risk_factor(self.start_date)
