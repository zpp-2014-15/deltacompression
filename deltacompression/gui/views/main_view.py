"""Main application view."""

import wx


from deltacompression.gui.views import experiment_panel
from deltacompression.gui.views import results_panel


class MainView(wx.Frame):
    """This view is responsible for choosing parameters and simulating."""

    _FRAME_TITLE = "Delta compression"

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title=self._FRAME_TITLE)

        self.views_keeper = None
        self.experiment_set_panel = None
        self.results_panel = None

        self.initUI()
        self.Centre()

    def initUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.views_keeper = wx.Notebook(self)

        self.experiment_set_panel = experiment_panel.ExperimentsPanel(self.views_keeper)
        self.views_keeper.AddPage(self.experiment_set_panel, 'Add an experiment')
        self.results_panel = results_panel.ResultsPanel(self.views_keeper)
        self.views_keeper.AddPage(self.results_panel, 'Results')

        sizer.Add(self.views_keeper, 1, wx.EXPAND)

        self.SetSizer(sizer)
