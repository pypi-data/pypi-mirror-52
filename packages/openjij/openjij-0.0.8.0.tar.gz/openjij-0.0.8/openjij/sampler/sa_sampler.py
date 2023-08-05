import numpy as np
import openjij
from openjij.sampler import measure_time
from openjij.sampler import BaseSampler
import cxxjij

from debtcollector import renames


class SASampler(BaseSampler):
    """Sampler with Simulated Annealing (SA).

    Inherits from :class:`openjij.sampler.sampler.BaseSampler`.

    Args:
        beta_min (float):
            Minmum beta (inverse temperature).

        beta_max (float):
            Maximum beta (inverse temperature).

        step_length (int):
            Number of annealing temperature divisions

        step_num (int):
            Number of steps per temperature.

        schedule_info (dict):
            Information about an annealing schedule.

        iteration (int):
            Number of iterations.

    Attributes:
        energy_bias (float):
            Energy bias.

        var_type (str):
            Type of variables: 'SPIN' or 'BINARY' which mean {-1, 1} or {0, 1}.

        indices (int):
            Indices of `openjij.model.model.BinaryQuadraticModel` object.

        N (int):
            Number of the indices.

    Raises:
        ValueError: If schedules or variables violate as below.
        - not list or numpy.array.
        - not list of tuple (beta : float, step_length : int).
        - beta is less than zero.

    """

    # @renames.renamed_kwarg(old_name='step_length', new_name='num_call_updater', removal_version='0.1.0')
    # @renames.renamed_kwarg(old_name='step_num', new_name='one_mc_step', removal_version='0.1.0')
    def __init__(self,
                 beta_min=0.1, beta_max=5.0,
                 step_num=10, step_length=100, schedule=None, iteration=1, **kwargs):


        if schedule:
            self.schedule = self._convert_validation_schedule(schedule)
            self.beta_min = None
            self.beta_max = None
            self.step_num = None
            self.step_length = None
            self.schedule_info = {'schedule': schedule}
        else:
            self.beta_min = beta_min
            self.beta_max = beta_max
            self.step_num = step_length 
            self.step_length = step_num 
            self.schedule = cxxjij.utility.make_classical_schedule_list(
                beta_min=beta_min, beta_max=beta_max,
                one_mc_step=step_num,
                num_call_updater=step_length
            )
            self.schedule_info = {
                'beta_min': beta_min, 'beta_max': beta_max,
                'step_num': step_num, 'step_length': step_length 
            }
        self.iteration = iteration

    def _convert_validation_schedule(self, schedule):
        if not isinstance(schedule, (list, np.array)):
            raise ValueError("schedule should be list or numpy.array")

        if isinstance(schedule[0], cxxjij.utility.ClassicalSchedule):
            return schedule

        if len(schedule[0]) != 2:
            raise ValueError(
                "schedule is list of tuple or list (beta : float, step_length : int)")

        # schedule validation  0 <= beta
        beta = np.array(schedule).T[0]
        if not np.all(0 <= beta):
            raise ValueError("schedule beta range is '0 <= beta'.")

        # convert to cxxjij.utility.ClassicalSchedule
        cxxjij_schedule = []
        for beta, step_length in schedule:
            _schedule = cxxjij.utility.ClassicalSchedule()
            _schedule.one_mc_step = step_length
            _schedule.updater_parameter.beta = beta
            cxxjij_schedule.append(_schedule)
        return cxxjij_schedule

    def _dict_to_model(self, var_type, h=None, J=None, Q=None, **kwargs):
        return openjij.BinaryQuadraticModel(h=h, J=J, Q=Q, var_type=var_type)

    def sample_ising(self, h, J,
                     initial_state=None, updater='single spin flip',
                     reinitilize_state=True, seed=None, **kwargs):
        """Sample from the specified Ising model.

        Args:
            h (dict):
                Linear biases of the Ising model.

            J (dict):
                Quadratic biases of the Ising model.

            initial_state (list):
                The initial state of simulated annealing

            updater (str):
                Monte Carlo update algorithm : 'single spin flip' or 'swendsenwang'

            reinitilize_state (bool):
                Reinitialize the initial state for every anneal-readout cycle.

            seed (:obj:`int`, optional):
                seed for Monte Carlo step

            **kwargs:
                Optional keyword arguments for the sampling method.

        Returns:
            :obj:: `openjij.sampler.response.Response` object.

        Examples:
            This example submits a two-variable Ising problem.

            >>> import openjij as oj
            >>> sampler = oj.SASampler()
            >>> response = sampler.sample_ising({0: -1, 1: 1}, {})
            >>> for sample in response.samples():    # doctest: +SKIP
            ...    print(sample)
            ...
            {0: 1, 1: -1}

        """
        model = self._dict_to_model(var_type=openjij.SPIN, h=h, J=J, **kwargs)
        return self.sampling(model,
                             initial_state=initial_state, updater=updater,
                             reinitilize_state=reinitilize_state,
                             seed=seed,
                             **kwargs
                             )

    def sample_qubo(self, Q,
                    initial_state=None, updater='single spin flip',
                    reinitilize_state=True, seed=None, **kwargs):
        """Sample from the specified QUBO.

        Args:
            Q (dict):
                Coefficients of a quadratic unconstrained binary optimization (QUBO) model.

            initial_state (list):
                The initial state of simulated annealing

            updater (str):
                Monte Carlo update algorithm : 'single spin flip' or 'swendsenwang'

            reinitilize_state (bool):
                Reinitialize the initial state for every anneal-readout cycle.

            seed (:obj:`int`, optional):
                seed for Monte Carlo step

            **kwargs:
                Optional keyword arguments for the sampling method.

        Returns:
            :obj:: `openjij.sampler.response.Response` object.

        Examples:
            This example submits a two-variable QUBO model.

            >>> import openjij as oj
            >>> sampler = oj.SASampler()
            >>> Q = {(0, 0): -1, (4, 4): -1, (0, 4): 2}
            >>> response = sampler.sample_qubo(Q)
            >>> for sample in response.samples():    # doctest: +SKIP
            ...    print(sample)
            ...
            {0: 0, 4: 1}

        """

        model = self._dict_to_model(var_type=openjij.BINARY, Q=Q, **kwargs)
        return self.sampling(model,
                             initial_state=initial_state, updater=updater,
                             reinitilize_state=reinitilize_state,
                             seed=seed,
                             **kwargs
                             )

    def sampling(self, model,
                 initial_state=None, updater='single spin flip',
                 reinitialize_state=True, seed=None,
                 **kwargs):

        ising_graph = model.get_cxxjij_ising_graph()

        # make init state generator
        if initial_state is None:
            if not reinitialize_state:
                raise ValueError(
                    'You need initial_state if reinitilize_state is False.')

            def _generate_init_state(): return ising_graph.gen_spin()
        else:
            # validate initial_state size
            if len(initial_state) != ising_graph.size():
                raise ValueError(
                    "the size of the initial state should be {}".format(ising_graph.size()))
            if model.var_type == openjij.SPIN:
                _init_state = np.array(initial_state)
            else:  # BINARY
                _init_state = (2*np.array(initial_state)-1).astype(np.int)

            def _generate_init_state(): return np.array(_init_state)

        # choose updater
        _updater_name = updater.lower().replace('_', '').replace(' ', '')
        if _updater_name == 'singlespinflip':
            algorithm = cxxjij.algorithm.Algorithm_SingleSpinFlip_run
            sa_system = cxxjij.system.make_classical_ising_Eigen(
                _generate_init_state(), ising_graph)
        elif _updater_name == 'swendsenwang':
            # swendsen-wang is not support Eigen system
            algorithm = cxxjij.algorithm.Algorithm_SwendsenWang_run
            sa_system = cxxjij.system.make_classical_ising(
                _generate_init_state(), ising_graph)
        else:
            raise ValueError(
                'updater is one of "single spin flip or swendsen wang"')

        response = self._sampling(
            model, _generate_init_state,
            algorithm, sa_system, initial_state,
            reinitialize_state, seed, **kwargs
        )

        response.update_ising_states_energies(
            response.states, response.energies)

        return response

    def _post_save(self, result_state, system, model, response):
        response.states.append(result_state)
        response.energies.append(model.calc_energy(
            result_state,
            need_to_convert_from_spin=True))
