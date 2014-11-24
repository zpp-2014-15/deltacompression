"""Main application view."""

import wx


class MainView(wx.Frame):
    """This view is responsible for choosing parameters and simulating."""

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Delta compression")
        self._simulate_button = None
        self._choose_data_button = None

    def buildFrame(self):
        """Creates frame with buttons and layout."""
        sizer = wx.BoxSizer(wx.VERTICAL)
        self._simulate_button = wx.Button(self, label="Simulate")
        sizer.Add(self._simulate_button, 0, wx.EXPAND | wx.ALL)

        self._choose_data_button = wx.Button(self, label="Choose data")
        sizer.Add(self._choose_data_button, 0, wx.EXPAND | wx.ALL)
        self.SetSizer(sizer)
        self.Centre()

    def getSimulateButton(self):
        return self._simulate_button

    def getChooseDataButton(self):
        return self._choose_data_button

    def _getDataFromDialog(self, dialog):
        if dialog.ShowModal() == wx.ID_OK:
            result = dialog.GetPath()
        else:
            result = ""

        dialog.Destroy()
        return result

    def getDataTestDirectory(self):
        """Allows user to choose directory.

        Returns:
            Absolute path or empty string if user canceled dialog.
        """
        dialog = wx.DirDialog(None, "Choose a directory:",
                              style=wx.DD_DEFAULT_STYLE)
        return self._getDataFromDialog(dialog)

    def getFilePath(self):
        """Allows user to choose file.

        Returns:
            Absolute path to file or empty string if user canceled dialog.
        """
        dialog = wx.FileDialog(None, "Choose a file:",
                               style=wx.DD_DEFAULT_STYLE)
        return self._getDataFromDialog(dialog)
