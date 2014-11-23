"""Main application controller."""


from deltacompression.gui.views import main_view

class MainController(object):

    def __init__(self, app):
        self._main_view = main_view.MainView(None)
        self._main_view.Show()
