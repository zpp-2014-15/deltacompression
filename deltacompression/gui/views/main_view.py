"""Main application view."""

import wx


from deltacompression.gui.views import experiment_panel


class MainView(wx.Frame):
    """This view is responsible for choosing parameters and simulating."""

    experiment_panel = None

    _FRAME_TITLE = "Delta compression"

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title=self._FRAME_TITLE)

        self.initUI()
        self.Centre()

    def initUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.experiment_panel = experiment_panel.ExperimentPanel(self)
        sizer.Add(self.experiment_panel, 0, wx.EXPAND | wx.ALL)

        self.SetSizer(sizer)
