"""Main application view."""

import wx


class MainView(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Delta compression")
        self._simulate_button = None

    def BuildFrame(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self._simulate_button = wx.Button(self, label="Simulate")
        sizer.Add(self._simulate_button, 0, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)

    def GetSimulateButton(self):
        return self._simulate_button
