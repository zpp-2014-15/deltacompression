"""Main application view."""

import wx


from deltacompression.gui.views import experiment_panel
from deltacompression.gui.views import result_panel


class MainView(wx.Frame):
    """This view is responsible for choosing parameters and simulating."""

    _FRAME_TITLE = "Delta compression"
    _FRAME_SIZE = (650, 400)
    _EXPERIMENT_PANEL = "Add Experiment"
    _RESULT_PANEL = "Results"

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title=self._FRAME_TITLE,
                          size=self._FRAME_SIZE)

        self.views_keeper = None
        self.experiment_panel = None
        self.result_panel = None

        self.initUI()
        self.Centre()

    def initUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.views_keeper = wx.Notebook(self)

        self.experiment_panel = experiment_panel.ExperimentPanel(
            self.views_keeper)
        self.views_keeper.AddPage(self.experiment_panel,
                                  self._EXPERIMENT_PANEL)
        self.result_panel = result_panel.ResultPanel(self.views_keeper)
        self.views_keeper.AddPage(self.result_panel, self._RESULT_PANEL)
        sizer.Add(self.views_keeper, 1, wx.EXPAND)

        self.SetSizer(sizer)
