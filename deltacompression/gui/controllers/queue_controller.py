"""Controls experiment model and view."""

from deltacompression.gui.models import experiment


class ExperimentQueueController(object):
    """Controller responsible for updating experiment and associated panel."""

    def __init__(self, main_controller, panel, experiment_queue):
        self._main_controller = main_controller
        self._exp_queue = experiment_queue
        self._panel = panel
        self._initSignals()
        self._panel.initializeWidgets(experiment_queue)
        experiment_queue.setController(self)

    def _initSignals(self):
        self._panel.Bind(self._panel.EVT_ADD_EXPERIMENT,
                         self._onAddTest)

    def _onAddTest(self, _):
        vers_dir = self._panel.getSelectedDir()
        if vers_dir:
            alg = self._panel.getSelectedAlgorithm()
            compr = self._panel.getSelectedCompression()
            exp = experiment.Experiment(self._exp_queue, vers_dir, alg, compr)

            self._panel.updateExperimentsList(
                self._exp_queue.getExperimentsList() + [exp])
            self._exp_queue.addExperiment(exp)

    def onExperimentPerformed(self, exp_result):
        self._panel.updateExperimentsList(self._exp_queue.getExperimentsList())
        self._main_controller.onExperimentPerformed(exp_result)
