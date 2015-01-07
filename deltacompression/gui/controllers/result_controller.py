class ResultSetController(object):
    def __init__(self, main_controller, panel, result_set):
        self._main_controller = main_controller
        self._result_set = result_set
        self._panel = panel

    def onExperimentPerformed(self, exp_result):
        self._panel.addResultToList(exp_result)
