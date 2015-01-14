"""Contains queue of experiments"""

from wx.lib.pubsub import Publisher


class ExperimentQueue(object):
    """Holds information about entire simulation
       (queue of experiments to be performed).
    """

    def getExperimentsList(self):
        raise NotImplementedError

    def addExperiment(self, experiment):
        raise NotImplementedError

    def removeExperiment(self, experiment):
        raise NotImplementedError


class DummyExperimentQueue(ExperimentQueue):
    """Performs experiments synchronically."""

    def __init__(self):
        self._experiment = None

    def getExperimentsList(self):
        return [self._experiment] if self._experiment else []

    def addExperiment(self, experiment):
        self._experiment = experiment
        Publisher().sendMessage("queue_changed")

        exp_result = experiment.run()
        self.removeExperiment(experiment)
        Publisher().sendMessage("experiment_performed", exp_result)
        Publisher().sendMessage("queue_changed")

    def removeExperiment(self, experiment):
        self._experiment = None
