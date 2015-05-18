"""Controls result list model and view."""

import pickle
import tempfile

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
        self._ser_errors = (pickle.PickleError, AttributeError, EOFError,
                            ImportError, IndexError, IOError)

    def _initSignals(self):
        self._panel.Bind(self._panel.EVT_ANALYSE, self._onAnalyseExperiments)
        self._panel.Bind(self._panel.EVT_LOAD, self._onLoadFile)
        self._panel.Bind(self._panel.EVT_SAVE, self._onSaveFile)

    def _checkValidity(self, results):
        if not results:
            return False
        ver = [n for n, _ in results[0].versions_with_results]
        for res in results:
            res_ver = [n for n, _ in res.versions_with_results]
            if ver != res_ver:
                return False
        return True

    def _getResults(self):
        checked = self._panel.getCheckedIndices()
        results = [self._result_list[i] for i in checked]
        return results

    def _onAnalyseExperiments(self, _):
        results = self._getResults()
        if not self._checkValidity(results):
            self._panel.onIncorrectItems()
            return

        chart = chart_view.BarChartView(results)
        chart.show()

    def _serialize(self, fil, results):
        pickle.dump(results, fil)

    def _deserialize(self, fil):
        return pickle.load(fil)

    def _onLoadFile(self, _):
        path = self._panel.getPath()
        try:
            with open(path, "r") as fil:
                new_results = self._deserialize(fil)
                for res in new_results:
                    self._addResult(res)
        except self._ser_errors:
            self._panel.onLoadError()


    def _onSaveFile(self, _):
        path = self._panel.getPath()
        results = self._getResults()
        try:
            with open(path, "w") as fil:
                self._serialize(fil, results)
        except self._ser_errors:
            self._panel.onSaveError()

    def _addResult(self, exp_result):
        self._panel.addResultToList(exp_result)
        self._result_list.append(exp_result)

    def onExperimentPerformed(self, exp_result):
        file_name = tempfile.mktemp(
            suffix=".{}".format(self._panel.getExtension()))
        res_file = open(file_name, "w")
        self._serialize(res_file, [exp_result])
        res_file.close()

        self._addResult(exp_result)
