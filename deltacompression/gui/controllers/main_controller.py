"""Main application controller."""

from deltacompression.gui.controllers import queue_controller
from deltacompression.gui.controllers import result_controller
from deltacompression.gui.models import queue
from deltacompression.gui.models import experiment_result
from deltacompression.gui.views import main_view


class MainController(object):
    """Responsible for updating models and changing views."""

    def __init__(self, app):
        self._exp_queue = queue.DummyExperimentQueue()
        self._result_list = experiment_result.ExperimentResultList()
        self._main_view = main_view.MainView(None)
        self._exp_controller = \
            queue_controller.ExperimentQueueController(
                self, self._main_view.experiment_panel, self._exp_queue)
        self._result_controller = result_controller.ResultSetController(
            self, self._main_view.result_panel, self._result_list)
        app.SetTopWindow(self._main_view)

    def startApp(self):
        """Shows main frame."""
        self._main_view.Show()

    def onExperimentPerformed(self, exp_result):
        self._result_controller.onExperimentPerformed(exp_result)
