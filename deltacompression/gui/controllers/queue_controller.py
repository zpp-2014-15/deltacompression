"""Controls experiment model and view."""

from wx.lib.pubsub import Publisher

from deltacompression.gui.models import experiment


class ExperimentQueueController(object):
    """Controller responsible for updating experiment and associated panel."""

    def __init__(self, main_controller, panel, experiment_queue):
        self._main_controller = main_controller
        self._exp_queue = experiment_queue
        self._panel = panel
        self._initSignals()

        experiment_instance = experiment.Experiment("path")
        self._panel.initializeWidgets(experiment_instance)


    def _initSignals(self):
        # Signal sent by user (view)
        self._panel.Bind(self._panel.EVT_ADD_EXPERIMENT,
                         self._onAddExperiment)

        # Signals sent by queue (model)
        Publisher().subscribe(self._onQueueChanged, "queue_changed")
        Publisher().subscribe(self._onExperimentPerformed,
                              "experiment_performed")

    def _onAddExperiment(self, _):
        vers_dir = self._panel.getSelectedDir()
        if vers_dir:
            alg = self._panel.getSelectedAlgorithm()
            compr = self._panel.getSelectedCompression()
            exp = experiment.Experiment(vers_dir, alg, compr)
            self._exp_queue.addExperiment(exp)

    def _onQueueChanged(self, _):
        self._panel.updateExperimentsList(self._exp_queue.getExperimentsList())

    def _onExperimentPerformed(self, msg):
        exp_result = msg.data
        self._main_controller.onExperimentPerformed(exp_result)
