"""Main application controller."""
import wx

from deltacompression.gui.views import main_view

class MainController(object):

    def __init__(self, app):
        self._main_view = main_view.MainView(None)

    def StartApp(self):
        self._main_view.BuildFrame()
        choose_data_button = self._main_view.GetChooseDataButton()
        choose_data_button.Bind(wx.EVT_BUTTON, self._ChooseFileHook)

        self._main_view.Show()

    def _ChooseFileHook(self, event):
        file_path = self._main_view.GetFilePath()
        print file_path
        # TODO(marcelzieba): Add FileProcessor to process data.
