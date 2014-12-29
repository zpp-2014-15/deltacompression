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
        test_nr = self._panel.getSelectedTest()
        test = self._experiment.getTest(test_nr)
        test.setAlgorithmName(alg)
        self._panel.updateAlgorithm(self._experiment)

    def _onCompressionSelected(self, _):
        compr = self._panel.getSelectedCompression()
        test_nr = self._panel.getSelectedTest()
        test = self._experiment.getTest(test_nr)
        test.setCompressionName(compr)
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
        result = self._experiment.runExperiment()
        # TODO: Handle result somehow
        print result.algorithm_name
        print result.compression_name
        print result.min_chunk
        print result.max_chunk
        print result.avg_chunk
        print result.files_with_results
