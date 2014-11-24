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

        self._choose_data_button = wx.Button(self, label="Choose data")
        sizer.Add(self._choose_data_button, 0, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)

    def GetSimulateButton(self):
        return self._simulate_button

    def GetChooseDataButton(self):
        return self._choose_data_button

    def _GetDataFromDialog(self, dialog):
        if dialog.ShowModal() == wx.ID_OK:
            result = dialog.GetPath()
        else:
            result = ""

        dialog.Destroy()
        return result

    def GetDataTestDirectory(self):
        """Allows user to choose directory.

        Returns:
            Absolute path or empty string if user canceled dialog.
        """
        dialog = wx.DirDialog(None, "Choose a directory:",
                              style=wx.DD_DEFAULT_STYLE)
        return self._GetDataFromDialog(dialog)

    def GetFilePath(self):
        """Allows user to choose file.

        Returns:
            Absolute path to file or empty string if user canceled dialog.
        """
        dialog = wx.FileDialog(None, "Choose a file:",
                              style=wx.DD_DEFAULT_STYLE)
        return self._GetDataFromDialog(dialog)
