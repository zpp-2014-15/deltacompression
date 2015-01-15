"""Contains queue of experiments"""

from wx.lib.pubsub import Publisher

from deltacompression.gui.controllers import queue_controller


class ExperimentQueue(object):
    """Holds information about entire simulation
       (queue of experiments to be performed).
    """

    def getExperimentsList(self):
        """Returns a list of experiments to be performed."""
        raise NotImplementedError

    def addExperiment(self, experiment):
        """Adds experiment to the queue so that it will be performed.

        Args:
            experiment: instance of Experiment
        """
        raise NotImplementedError

    def _sendQueueChangedEvt(self):
        """Sends a signal to the controller."""
        Publisher().sendMessage(
            queue_controller.ExperimentQueueController.EVT_QUEUE_CHANGED)

    def _sendExperimentPerformedEvt(self, exp_result):
        """Sends a signal to the controller."""
        Publisher().sendMessage(
            queue_controller.ExperimentQueueController. \
            EVT_EXPERIMENT_PERFORMED,
            exp_result)


class DummyExperimentQueue(ExperimentQueue):
    """Performs experiments synchronically."""

    def __init__(self):
        self._experiment = None

    def getExperimentsList(self):
        return [self._experiment] if self._experiment else []

    def addExperiment(self, experiment):
        self._experiment = experiment
        self._sendQueueChangedEvt()

        exp_result = experiment.run()
        self._experiment = None
        self._sendExperimentPerformedEvt(exp_result)
        self._sendQueueChangedEvt()
