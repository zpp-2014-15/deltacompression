"""Controls result list model and view."""

from deltacompression.gui.views import chart_view


class ResultController(object):
    """Controller responsible for updating results' model and view."""
    def __init__(self, main_controller, panel, result_list):
        """Creates ResultController object.

        Args:
            main_controller: instance of MainController.
            panel: instance of ResultPanel.
            result_list: list of ExperimentResult objects.
        """
        self._main_controller = main_controller
        self._result_list = result_list
        self._panel = panel
        self._initSignals()

    def _initSignals(self):
        self._panel.Bind(self._panel.EVT_ANALYSE, self._onAnalyseExperiments)

    def _checkValidity(self, results):
        if not results:
            return False
        ver = [n for n, _ in results[0].versions_with_results]
        for res in results:
            res_ver = [n for n, _ in res.versions_with_results]
            if ver != res_ver:
                return False
        return True

    def _onAnalyseExperiments(self, _):
        checked = self._panel.getCheckedIndices()

        results = [self._result_list[i] for i in checked]

        if not self._checkValidity(results):
            self._panel.onIncorrectItems()
            return

        chart = chart_view.BarChartView(results)
        chart.show()

    def onExperimentPerformed(self, exp_result):
        self._panel.addResultToList(exp_result)
        self._result_list.append(exp_result)
