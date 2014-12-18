"""Controls experiment model and view."""


class ExperimentController(object):
    """Controller responsible for updating experiment and associated panel."""

    def __init__(self, panel, experiment):
        self._experiment = experiment
        def_alg = self._experiment.algorithm_factory.DUMMY_ALGORITHM
        def_comp = self._experiment.compression_factory.DUMMY_COMPRESSION
        self._experiment.setAlgorithmName(def_alg)
        self._experiment.setCompressionName(def_comp)
        self._panel = panel
        self._initSignals()
        self._updatePanel()

    def _initSignals(self):
        self._panel.Bind(self._panel.EVT_ALGORITHM_SELECTED,
                         self._onAlgorithmSelected)
        self._panel.Bind(self._panel.EVT_ADD_FILE,
                         self._onAddFile)
        self._panel.Bind(self._panel.EVT_SIMULATE,
                         self._onSimulate)
        self._panel.Bind(self._panel.EVT_COMPRESSION_SELECTED,
                         self._onCompressionSelected)

    def _updatePanel(self):
        self._panel.updateExperiment(self._experiment)

    def _onAlgorithmSelected(self, _):
        alg = self._panel.getSelectedAlgorithm()
        self._experiment.setAlgorithmName(alg)
        self._updatePanel()

    def _onCompressionSelected(self, _):
        compression = self._panel.getSelectedCompression()
        self._experiment.setCompressionName(compression)
        self._updatePanel()

    def _onAddFile(self, _):
        vers_dir = self._panel.getDirectory()
        if vers_dir:
            #self._experiment.addFileToList(new_file)
            self._experiment.setVersionsDir(vers_dir)
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
