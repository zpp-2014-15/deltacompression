"""Main application view."""

import wx


class MainView(wx.Frame):
    """This view is responsible for choosing parameters and simulating."""

    _FRAME_TITLE = "Delta compression"
    _CHOOSE_DATA_BUTTON = "Choose data"
    _SIMULATE_BUTTON = "Add to backup system"
    _DATA_TO_SEND = "Data to send: %.3f MB."
    _CHOSEN_FILE = "File to add to backup system: %s"
    _FILE_CHOOSE_DIALOG_TITLE = "Choose a file:"
    _DIRECTORY_CHOOSE_DIALOG_TITLE = "Choose a directory:"

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title=self._FRAME_TITLE)
        self._choose_data_button = None
        self._chosen_file_label = None
        self._simulate_button = None
        self._result_length_label = None

    def buildFrame(self):
        """Creates frame with buttons and layout."""
        sizer = wx.BoxSizer(wx.VERTICAL)
        self._choose_data_button = wx.Button(self,
                                             label=self._CHOOSE_DATA_BUTTON)
        sizer.Add(self._choose_data_button, 0, wx.EXPAND | wx.ALL)

        self._chosen_file_label = wx.StaticText(self,
                                                label=self._CHOSEN_FILE % None)
        sizer.Add(self._chosen_file_label)

        self._simulate_button = wx.Button(self, label=self._SIMULATE_BUTTON)
        sizer.Add(self._simulate_button, 0, wx.EXPAND | wx.ALL)

        self._result_length_label = wx.StaticText(self,
                                                  label=self._DATA_TO_SEND % 0)
        sizer.Add(self._result_length_label)
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

    def setChosenFile(self, chosen_file):
        self._chosen_file_label.SetLabel(self._CHOSEN_FILE % chosen_file)

    def setLengthOfDataToSend(self, length):
        length_in_mb = float(length) / 1024 / 1024
        self._result_length_label.SetLabel(self._DATA_TO_SEND % length_in_mb)

    def getDataTestDirectory(self):
        """Allows user to choose directory.

        Returns:
            Absolute path or empty string if user canceled dialog.
        """
        dialog = wx.DirDialog(None, self._DIRECTORY_CHOOSE_DIALOG_TITLE,
                              style=wx.DD_DEFAULT_STYLE)
        return self._getDataFromDialog(dialog)

    def getFilePath(self):
        """Allows user to choose file.

        Returns:
            Absolute path to file or empty string if user canceled dialog.
        """
        dialog = wx.FileDialog(None, self._FILE_CHOOSE_DIALOG_TITLE,
                               style=wx.DD_DEFAULT_STYLE)
        return self._getDataFromDialog(dialog)
