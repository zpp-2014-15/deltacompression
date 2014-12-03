"""Controls experiment model and view."""


class ExperimentController(object):

    def __init__(self, panel, experiment):
        self._experiment = experiment
        self._panel = panel
        self._panel.updateExperiment(self._experiment)
