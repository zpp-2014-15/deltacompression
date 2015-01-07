"""Controls experiment model and view."""

from deltacompression.gui.models import experiment


class ExperimentSetController(object):
    """Controller responsible for updating experiment and associated panel."""

    def __init__(self, main_controller, panel, experiment_set):
        self._main_controller = main_controller
        self._experiment_set = experiment_set
        self._panel = panel
        self._initSignals()
        self._panel.initializeWidgets(experiment_set)
        experiment_set.setController(self)

    def _initSignals(self):
        self._panel.Bind(self._panel.EVT_ADD_TEST,
                         self._onAddTest)
        self._panel.Bind(self._panel.EVT_SIMULATE,
                         self._onSimulate)

    def _onAddTest(self, _):
        vers_dir = self._panel.getDirectory()
        if vers_dir:
            alg = self._panel.getSelectedAlgorithm()
            compr = self._panel.getSelectedCompression()
            new_experiment = experiment.Experiment(self._experiment_set,
                vers_dir, alg, compr)

            self._experiment_set.addExperimentToList(new_experiment)
            self._panel.addExperimentToList(new_experiment)

    def _onSimulate(self, _):
        results = self._experiment_set.runExperiments()
        # TODO: Handle result somehow
        for test_result in results:
            print test_result.algorithm_name
            print test_result.compression_name
            print test_result.min_chunk
            print test_result.max_chunk
            print test_result.avg_chunk
            print test_result.versions_with_results

    def onExperimentPerformed(self, exp_result):
        self._panel.removeExperimentFromList(0)
        self._main_controller.onExperimentPerformed(exp_result)
