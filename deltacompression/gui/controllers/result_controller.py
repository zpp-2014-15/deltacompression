"""Controls result list model and view."""


class ResultSetController(object):
    """Controller responsible for updating results' model and view."""
    def __init__(self, main_controller, panel, result_set):
        self._main_controller = main_controller
        self._result_set = result_set
        self._panel = panel
        self._initSignals()

    def _initSignals(self):
        self._panel.Bind(self._panel.EVT_ANALYSE, self._onAnalyseExperiments)

    def _onAnalyseExperiments(self, _):
        items_checked = self._panel.getCheckedResults()
        # combine with charts
        for index in items_checked:
            result = self._result_set.getNthResult(index)
            result.printData()

    def onExperimentPerformed(self, exp_result):
        self._panel.addResultToList(exp_result)
        self._result_set.addResultToList(exp_result)

