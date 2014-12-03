"""Main application view."""

import wx


from deltacompression.gui.views import experiment_panel


class MainView(wx.Frame):
    """This view is responsible for choosing parameters and simulating."""

    experiment_panel = None

    _FRAME_TITLE = "Delta compression"
    _CHOOSE_DATA_BUTTON = "Choose data"
    _SIMULATE_BUTTON = "Add to backup system"
    _DATA_TO_SEND = "Data to send: %.3f MB."
    _CHOSEN_FILE = "File to add to backup system: %s"
    _FILE_CHOOSE_DIALOG_TITLE = "Choose a file:"
    _DIRECTORY_CHOOSE_DIALOG_TITLE = "Choose a directory:"

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title=self._FRAME_TITLE)

        self.initUI()
        self.Centre()

    def initUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.experiment_panel = experiment_panel.ExperimentPanel(self)
        sizer.Add(self.experiment_panel, 0, wx.EXPAND | wx.ALL)

        self.SetSizer(sizer)

        """
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

        self._experiment = experiment_panel.ExperimentPanel(self)

        self.Centre()
        """

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
