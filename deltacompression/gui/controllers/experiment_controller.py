"""Controls experiment model and view."""

from deltacompression.gui.models import test


class ExperimentController(object):
    """Controller responsible for updating experiment and associated panel."""

    def __init__(self, panel, experiment):
        self._experiment = experiment
        self._panel = panel
        self._initSignals()
        self._panel.initializeExperiment(experiment)

    def _initSignals(self):
        self._panel.Bind(self._panel.EVT_ALGORITHM_SELECTED,
                         self._onAlgorithmSelected)
        self._panel.Bind(self._panel.EVT_COMPRESSION_SELECTED,
                         self._onCompressionSelected)
        self._panel.Bind(self._panel.EVT_TEST_SELECTED,
                         self._onTestSelected)
        self._panel.Bind(self._panel.EVT_ADD_TEST,
                         self._onAddTest)
        self._panel.Bind(self._panel.EVT_REMOVE_TEST,
                         self._onRemoveTest)
        self._panel.Bind(self._panel.EVT_SIMULATE,
                         self._onSimulate)

    def _onAlgorithmSelected(self, _):
        alg = self._panel.getSelectedAlgorithm()
        selected_test_nr = self._panel.getSelectedTest()
        selected_test = self._experiment.getTest(selected_test_nr)
        selected_test.setAlgorithmName(alg)
        self._panel.updateAlgorithm(self._experiment)

    def _onCompressionSelected(self, _):
        compr = self._panel.getSelectedCompression()
        selected_test_nr = self._panel.getSelectedTest()
        selected_test = self._experiment.getTest(selected_test_nr)
        selected_test.setCompressionName(compr)
        self._panel.updateCompression(self._experiment)

    def _onAddTest(self, _):
        vers_dir = self._panel.getDirectory()
        if vers_dir:
            new_test = test.Test(vers_dir, self._experiment)
            self._experiment.addTestToList(new_test)
            self._panel.addTestToList(new_test)

    def _onRemoveTest(self, _):
        test_nr = self._panel.getSelectedTest()
        self._experiment.removeTestFromList(test_nr)
        self._panel.removeTestFromList(test_nr)

    def _onTestSelected(self, _):
        self._panel.updateAlgorithm(self._experiment)
        self._panel.updateCompression(self._experiment)

    def _onSimulate(self, _):
        results = self._experiment.runExperiment()
        # TODO: Handle result somehow
        for test_result in results:
            print test_result.algorithm_name
            print test_result.compression_name
            print test_result.min_chunk
            print test_result.max_chunk
            print test_result.avg_chunk
            print test_result.versions_with_results
