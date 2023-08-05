import os
import pickle

import autofit.optimize.non_linear.multi_nest
import autofit.optimize.non_linear.non_linear
from autofit import conf
from autofit import exc
from autofit.optimize import grid_search
from autofit.tools.promise import PromiseResult


class HyperPhase(object):
    pass


class AbstractPhase(object):

    def __init__(
            self,
            phase_name,
            phase_tag=None,
            phase_folders=tuple(),
            optimizer_class=autofit.optimize.non_linear.multi_nest.MultiNest,
            auto_link_priors=False
    ):
        """
        A phase in an lensing pipeline. Uses the set non_linear optimizer to try to
        fit_normal models and image passed to it.

        Parameters
        ----------
        optimizer_class: class
            The class of a non_linear optimizer
        phase_name: str
            The name of this phase
        """
        if phase_tag is not None:
            self.phase_tag = phase_tag
        else:
            self.phase_tag = ''

        self.optimizer = optimizer_class(
            phase_name=phase_name,
            phase_tag=phase_tag,
            phase_folders=phase_folders
        )
        self.auto_link_priors = auto_link_priors

    @property
    def result(self):
        return PromiseResult(self)

    @property
    def phase_path(self):
        return self.optimizer.phase_path

    @phase_path.setter
    def phase_path(self, phase_path):
        self.optimizer.phase_path = phase_path

    @property
    def phase_name(self):
        return self.optimizer.phase_name

    @phase_name.setter
    def phase_name(self, phase_name):
        self.optimizer.phase_name = phase_name

    @property
    def variable(self):
        """
        Convenience method

        Returns
        -------
        ModelMapper
            A model mapper comprising all the variable (prior) objects in this lensing
        """
        return self.optimizer.variable

    @variable.setter
    def variable(self, variable):
        self.optimizer.variable = variable

    def run_analysis(self, analysis):
        return self.optimizer.fit(analysis)

    @property
    def path(self):
        return self.optimizer.path

    @property
    def doc(self):
        if self.__doc__ is not None:
            return self.__doc__.replace("  ", "").replace("\n", " ")

    def customize_priors(self, results):
        """
        Perform any prior or constant passing. This could involve setting model
        attributes equal to priors or constants from a previous phase.

        Parameters
        ----------
        results: ResultsCollection
            The result of the previous phase
        """
        pass

    # noinspection PyAbstractClass
    class Analysis(autofit.optimize.non_linear.non_linear.Analysis):

        def __init__(self, results=None):
            """
            An lensing object

            Parameters
            ----------
            results: ResultsCollection
                The results of all previous phases
            """

            self.results = results

        @property
        def last_results(self):
            if self.results is not None:
                return self.results.last

    def make_result(self, result, analysis):
        raise NotImplementedError()

    def make_optimizer_pickle_path(self) -> str:
        """
        Create the path at which the optimizer pickle should be saved
        """
        return "{}/optimizer.pickle".format(self.make_path())

    def make_path(self) -> str:
        """
        Create the path to the folder at which the metadata and optimizer pickle should
        be saved
        """
        return "{}/{}/{}/{}/".format(conf.instance.output_path, self.phase_path,
                                     self.phase_name, self.phase_tag)

    def save_optimizer_for_phase(self):
        """
        Save the optimizer associated with the phase as a pickle
        """
        with open(self.make_optimizer_pickle_path(), "w+b") as f:
            f.write(pickle.dumps(self.optimizer))

    def save_metadata(self, data_name, pipeline_name):
        """
        Save metadata associated with the phase, such as the name of the pipeline, the
        name of the phase and the name of the data being fit
        """
        with open("{}/metadata".format(self.make_path()), "w+") as f:
            f.write(
                "pipeline={}\nphase={}\ndata={}".format(pipeline_name, self.phase_name,
                                                        data_name))

    def assert_optimizer_pickle_matches_for_phase(self):
        """
        Assert that the previously saved optimizer is equal to the phase's optimizer if
        a saved optimizer is found.

        Raises
        -------
        exc.PipelineException
        """
        path = self.make_optimizer_pickle_path()
        if os.path.exists(path):
            with open(path, "r+b") as f:
                loaded_optimizer = pickle.loads(f.read())
                if self.optimizer != loaded_optimizer:
                    raise exc.PipelineException(
                        f"Can't restart phase at path {path} because settings don't "
                        f"match. Did you change the optimizer settings or model?")

    def assert_and_save_pickle(self):
        if conf.instance.general.get("output", "assert_pickle_matches", bool):
            self.assert_optimizer_pickle_matches_for_phase()
        self.save_optimizer_for_phase()


def as_grid_search(phase_class, parallel=False):
    """
    Create a grid search phase class from a regular phase class. Instead of the phase
    being optimised by a single non-linear optimiser, a new optimiser is created for
    each square in a grid.

    Parameters
    ----------
    phase_class
        The original phase class
    parallel: bool
        Indicates whether non linear searches in the grid should be performed on
        parallel processes.

    Returns
    -------
    grid_search_phase_class: GridSearchExtension
        A class that inherits from the original class, replacing the optimiser with a
        grid search optimiser.

    """

    class GridSearchExtension(phase_class):
        def __init__(self, *args, phase_name, phase_folders=tuple(),
                     number_of_steps=10,
                     optimizer_class=autofit.optimize.non_linear.multi_nest.MultiNest,
                     **kwargs):
            super().__init__(*args, phase_name=phase_name,
                             phase_folders=phase_folders,
                             optimizer_class=optimizer_class, **kwargs)
            self.optimizer = grid_search.GridSearch(phase_name=phase_name,
                                                    phase_tag=self.phase_tag,
                                                    phase_folders=phase_folders,
                                                    number_of_steps=number_of_steps,
                                                    optimizer_class=optimizer_class,
                                                    model_mapper=self.variable,
                                                    parallel=parallel)

        def run_analysis(self, analysis):
            return self.optimizer.fit(analysis, self.grid_priors)

        # noinspection PyMethodMayBeStatic,PyUnusedLocal
        def make_result(self, result, analysis):
            return result

        @property
        def grid_priors(self):
            raise NotImplementedError(
                "The grid priors property must be implemented to provide a list of "
                "priors to be grid searched")

    return GridSearchExtension
