"""Contains queue of experiments"""
import threading
import wx

from wx.lib.pubsub import Publisher # pylint: disable=E0611

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
            experiment: instance of Experiment.
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


class ThreadEvent(wx.PyCommandEvent):

    evt_EXECUTED = wx.NewEventType()
    EVT_EXECUTED = wx.PyEventBinder(evt_EXECUTED)

    def __init__(self, value=None):
        super(ThreadEvent, self).__init__(self.evt_EXECUTED, -1)
        self._value = value

    def getValue(self):
        return self._value


class ExperimentThread(threading.Thread):
    def __init__(self, parent, experiment):
        threading.Thread.__init__(self)
        self._parent = parent
        self._experiment = experiment

    def run(self):
        exp_result = self._experiment.run()
        evt = ThreadEvent(exp_result)
        wx.PostEvent(self._parent, evt)


class AsyncExperimentQueue(ExperimentQueue, wx.EvtHandler):
    """Performs experiments synchronically."""

    def __init__(self):
        super(AsyncExperimentQueue, self).__init__()
        self._experiments = []
        self.Bind(ThreadEvent.EVT_EXECUTED, self._onExecuted)

    def getExperimentsList(self):
        return self._experiments

    def addExperiment(self, experiment):
        self._experiments.append(experiment)
        self._sendQueueChangedEvt()

        if len(self._experiments) == 1:
            self._runNextExperiment()

    def _runNextExperiment(self):
        thread = ExperimentThread(self, self._experiments[0])
        thread.start()

    def _onExecuted(self, evt):
        exp_result = evt.getValue()
        self._experiments.pop(0)
        self._sendExperimentPerformedEvt(exp_result)
        self._sendQueueChangedEvt()

        if len(self._experiments) > 0:
            self._runNextExperiment()


