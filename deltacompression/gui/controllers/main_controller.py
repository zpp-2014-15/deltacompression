"""Main application controller."""

from deltacompression.gui.controllers import experiment_controller
from deltacompression.gui.models import experiment
from deltacompression.gui.views import main_view


class MainController(object):
    """Responsible for updating models and changing views."""

    def __init__(self, app):
        self._experiment = experiment.Experiment()
        self._main_view = main_view.MainView(None)
        self._experiment_controller = \
            experiment_controller.ExperimentController(
                self._main_view.experiment_panel, self._experiment)
        app.SetTopWindow(self._main_view)

    def startApp(self):
        """Shows main frame."""
        self._main_view.Show()
