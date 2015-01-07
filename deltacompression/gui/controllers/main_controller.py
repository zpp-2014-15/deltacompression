"""Main application controller."""

from deltacompression.gui.controllers import experiment_controller
from deltacompression.gui.controllers import result_controller
from deltacompression.gui.models import experiment
from deltacompression.gui.models import experiment_result
from deltacompression.gui.views import main_view


class MainController(object):
    """Responsible for updating models and changing views."""

    def __init__(self, app):
        self._experiment_set = experiment.ExperimentSet()
        self._result_set = experiment_result.ExperimentResultSet()
        self._main_view = main_view.MainView(None)
        self._experiment_set_controller = \
            experiment_controller.ExperimentSetController(
                self, self._main_view.experiment_set_panel, self._experiment_set)
        self._result_set_controller = result_controller.ResultSetController(
            self, self._main_view.results_panel, self._result_set)
        app.SetTopWindow(self._main_view)

    def startApp(self):
        """Shows main frame."""
        self._main_view.Show()

    def onExperimentPerformed(self, exp_result):
        self._result_set_controller.onExperimentPerformed(exp_result)
