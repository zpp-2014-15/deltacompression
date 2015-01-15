"""Controls experiment model and view."""

from wx.lib.pubsub import Publisher # pylint: disable=E0611

from deltacompression.gui.models import experiment


class ExperimentQueueController(object):
    """Controller responsible for updating experiment and associated panel

    Attributes:
        EVT_QUEUE_CHANGED: String, name of the Publisher topic.
        EVT_EXPERIMENT_PERFORMED: String, name of the Publisher topic.
    """

    EVT_QUEUE_CHANGED = 'queue_changed'
    EVT_EXPERIMENT_PERFORMED = 'experiment_performed'

    def __init__(self, main_controller, panel, experiment_queue):
        """Creates ExperimentQueueController object.

        Args:
            main_controller: instance of MainController.
            panel: instance of ExperimentPanel.
            experiment_queue: instance of ExperimentQueue.
        """
        self._main_controller = main_controller
        self._exp_queue = experiment_queue
        self._panel = panel
        self._initSignals()

    def _initSignals(self):
        # Signal sent by user (view)
        self._panel.Bind(self._panel.EVT_ADD_EXPERIMENT,
                         self._onAddExperiment)

        # Signals sent by queue (model)
        Publisher().subscribe(self._onQueueChanged, self.EVT_QUEUE_CHANGED)
        Publisher().subscribe(self._onExperimentPerformed,
                              self.EVT_EXPERIMENT_PERFORMED)

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
