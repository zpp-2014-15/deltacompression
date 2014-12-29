"""Controls experiment model and view."""

from deltacompression.gui.models import test


class ExperimentController(object):
    """Controller responsible for updating experiment and associated panel."""

    def __init__(self, panel, experiment):
        self._experiment = experiment
        def_alg = self._experiment.algorithm_factory.DUMMY_ALGORITHM
        def_comp = self._experiment.compression_factory.DUMMY_COMPRESSION
        #self._experiment.setAlgorithmName(def_alg)
        #self._experiment.setCompressionName(def_comp)
        self._panel = panel
        self._initSignals()
        self._updatePanel()

    def _initSignals(self):
        self._panel.Bind(self._panel.EVT_ALGORITHM_SELECTED,
                         self._onAlgorithmSelected)
        self._panel.Bind(self._panel.EVT_COMPRESSION_SELECTED,
                         self._onCompressionSelected)
        self._panel.Bind(self._panel.EVT_ADD_TEST,
                         self._onAddTest)
        self._panel.Bind(self._panel.EVT_SIMULATE,
                         self._onSimulate)
        self._panel.Bind(self._panel.EVT_TEST_SELECTED,
                         self._onTestSelected)

    def _updatePanel(self):
        self._panel.updateExperiment(self._experiment)

    def _onAlgorithmSelected(self, _):
        alg = self._panel.getSelectedAlgorithm()
        test = self._experiment.getSelectedTest()
        test.setAlgorithmName(alg)
        self._updatePanel()

    def _onCompressionSelected(self, _):
        compr = self._panel.getSelectedCompression()
        test = self._experiment.getSelectedTest()
        test.setCompressionName(compr)
        self._updatePanel()

    def _onTestSelected(self, _):
        test_nr = self._panel.getSelectedTest()
        self._experiment.setSelectedTest(test_nr)
        self._updatePanel()

    def _onAddTest(self, _):
        vers_dir = self._panel.getDirectory()
        if vers_dir:
            new_test = test.Test(vers_dir, self._experiment)
            self._experiment.addTestToList(new_test)
            self._experiment.setSelectedTest(self._experiment.getTestsNr() - 1)
            self._updatePanel()

    def _onSimulate(self, _):
        result = self._experiment.runExperiment()
        # TODO: Handle result somehow
        print result.algorithm_name
        print result.compression_name
        print result.min_chunk
        print result.max_chunk
        print result.avg_chunk
        print result.files_with_results
