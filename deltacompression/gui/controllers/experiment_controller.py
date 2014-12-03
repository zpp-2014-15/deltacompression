"""Controls experiment model and view."""


class ExperimentController(object):
    """Controller responsible for updating experiment and associated panel."""

    def __init__(self, panel, experiment):
        self._experiment = experiment
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

    def _updatePanel(self):
        self._panel.updateExperiment(self._experiment)

    def _onAlgorithmSelected(self, _):
        alg = self._panel.getSelectedAlgorithm()
        self._experiment.setAlgorithmName(alg)
        self._updatePanel()

    def _onAddFile(self, _):
        new_file = self._panel.getFile()
        if new_file:
            self._experiment.addFileToList(new_file)
            self._updatePanel()

    def _onSimulate(self, _):
        result = self._experiment.runExperiment()
        # TODO: Handle result somehow better
        print result.algorithm_name
        print result.compression_name
        print result.min_chunk
        print result.max_chunk
        print result.files_with_results
