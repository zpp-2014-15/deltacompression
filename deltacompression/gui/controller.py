"""Main application controller."""
import wx

from deltacompression.gui.views import main_view


class MainController(object):

    def __init__(self, app):
        self._main_view = main_view.MainView(None)
        app.SetTopWindow(self._main_view)

    def startApp(self):
        """Creates main Frame and shows this frame."""
        self._main_view.buildFrame()
        choose_data_button = self._main_view.getChooseDataButton()
        choose_data_button.Bind(wx.EVT_BUTTON, self._chooseFileHook)

        self._main_view.Show()

    def _chooseFileHook(self, _):
        """Shows dialog to choose file."""
        file_path = self._main_view.getFilePath()
        print file_path
        # TODO(marcelzieba): Add FileProcessor to process data.
