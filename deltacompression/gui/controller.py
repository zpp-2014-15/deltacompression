"""Main application controller."""
import wx

from deltacompression.gui.views import main_view

class MainController(object):

    def __init__(self, app):
        self._main_view = main_view.MainView(None)

    def StartApp(self):
        self._main_view.BuildFrame()
        choose_data_button = self._main_view.GetChooseDataButton()
        choose_data_button.Bind(wx.EVT_BUTTON, self._ChooseDirectoryHook)

        self._main_view.Show()

    def _ChooseDirectoryHook(self, event):
        directory = self._main_view.GetDataTestDirectory()
        print directory
