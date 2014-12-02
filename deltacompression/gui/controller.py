"""Main application controller."""
import wx

from deltacompression.backend import compression_algorithm
from deltacompression.backend import data_updater
from deltacompression.backend import file_processor
from deltacompression.backend import chunk_hash
from deltacompression.backend import storage
from deltacompression.gui.views import main_view


class MainController(object):
    """Responsible for updating models and changing views."""

    _MIN_CHUNK = 1024
    _MAX_CHUNK = 10240

    def __init__(self, app):
        self._main_view = main_view.MainView(None)
        app.SetTopWindow(self._main_view)

        self._storage = storage.Storage(chunk_hash.HashSHA256(), None)
        self._compression = compression_algorithm.DummyCompressionAlgorithm()
        self._updater = data_updater.DummyUpdater(self._storage)
        self._file_processor = file_processor.FileProcessor(self._updater,
                                                            self._compression,
                                                            self._MIN_CHUNK,
                                                            self._MAX_CHUNK)
        self._chosen_file = None

    def startApp(self):
        """Creates main Frame and shows this frame."""
        self._main_view.buildFrame()
        choose_data_button = self._main_view.getChooseDataButton()
        choose_data_button.Bind(wx.EVT_BUTTON, self._chooseFileHook)

        simulate_button = self._main_view.getSimulateButton()
        simulate_button.Bind(wx.EVT_BUTTON, self._clickSimulateHook)

        self._main_view.Show()

    def _clickSimulateHook(self, _):
        if self._chosen_file:
            returned_data = self._file_processor.processFile(self._chosen_file)
            # This is not actually MVC architecture. MVC architecture needs
            # quite a lot more work. I want to do this later.
            print len(returned_data)
            self._main_view.setLengthOfDataToSend(len(returned_data))

    def _chooseFileHook(self, _):
        """Shows dialog to choose file."""
        file_path = self._main_view.getFilePath()
        if file_path:
            self._chosen_file = file_path
            self._main_view.setChosenFile(self._chosen_file)
