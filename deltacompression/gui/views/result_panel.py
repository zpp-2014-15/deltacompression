"""This module contains panel for viewing experiment results."""
import wx
import sys

from deltacompression.gui.views import utils


class ResultPanel(wx.Panel):
    """Displays result list and allows to analyse selected results.

    Attributes:
        evt_ANALYSE: event meaning that analyse button was clicked.
        EVT_ANALYSE: evt_ANALYSE's binder.

        _ANALYSE: String, name of the analyse button.
        _SELECT_ALL: String, name of select_all_button.
        _DESELECT_ALL: String, name of deselect_all_button.
    """

    evt_ANALYSE = wx.NewEventType()
    EVT_ANALYSE = wx.PyEventBinder(evt_ANALYSE)
    evt_SAVE = wx.NewEventType()
    EVT_SAVE = wx.PyEventBinder(evt_SAVE)
    evt_LOAD = wx.NewEventType()
    EVT_LOAD = wx.PyEventBinder(evt_LOAD)

    _ANALYSE = "Analyse"
    _SELECT_ALL = "Select all"
    _DESELECT_ALL = "Deselect all"
    _INCORRECT_ITEMS = ("The set of versions should be the same for all of "
                        "the experiments and there should be at least one "
                        "experiment.")

    _SAVE = "Save to a file"
    _LOAD = "Load from a file"
    _CHOOSE_FILE_TO_LOAD = "Choose a file"
    _CHOOSE_FILE_TO_SAVE = "Save a file"
    _EXTENSION = "kzl"
    _FILE_FORMAT = "{UP} files (*.{LO})|*.{LO}".format(UP=_EXTENSION.upper(),
                                                       LO=_EXTENSION)
    _CANT_SAVE = "Cannot save data in file {}"
    _CANT_LOAD = "Cannot load data from file {}"
    _DEF_FILE_NAME = "*.{}".format(_EXTENSION)

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._results_list = None
        self._select_all_button = None
        self._deselect_all_button = None
        self._analyse_button = None
        self._save_button = None
        self._load_button = None
        self._path = None

        self._initUI()

    def _initUI(self):
        """Initializes all controls."""
        sizer = wx.BoxSizer(wx.VERTICAL)

        self._results_list = utils.CheckListCtrl(self)
        self._results_list.InsertColumn(0, "Path")
        self._results_list.InsertColumn(1, "Algorithm", width=200)
        self._results_list.InsertColumn(2, "Compression", width=150)
        sizer.Add(self._results_list, 1, wx.EXPAND)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self._select_all_button = wx.Button(self, label=self._SELECT_ALL)
        self._select_all_button.Bind(wx.EVT_BUTTON, self._onSelectAll)

        self._deselect_all_button = wx.Button(self, label=self._DESELECT_ALL)
        self._deselect_all_button.Bind(wx.EVT_BUTTON, self._onDeselectAll)

        hbox.Add(self._select_all_button, 1, wx.EXPAND)
        hbox.Add(self._deselect_all_button, 1, wx.EXPAND)
        sizer.Add(hbox, 0, wx.EXPAND)

        action_hbox = wx.BoxSizer(wx.HORIZONTAL)
        self._analyse_button = wx.Button(self, label=self._ANALYSE,
                                         size=(-1, 50))
        self._save_button = wx.Button(self, label=self._SAVE, size=(-1, 50))
        self._load_button = wx.Button(self, label=self._LOAD, size=(-1, 50))

        self._analyse_button.Bind(wx.EVT_BUTTON, self._onClickAnalyse)
        self._load_button.Bind(wx.EVT_BUTTON, self._onClickLoad)
        self._save_button.Bind(wx.EVT_BUTTON, self._onClickSave)

        action_hbox.Add(self._analyse_button, 1, wx.EXPAND)
        action_hbox.Add(self._save_button, 1, wx.EXPAND)
        action_hbox.Add(self._load_button, 1, wx.EXPAND)

        sizer.Add(action_hbox, 0, wx.EXPAND)

        self.SetSizer(sizer)

    def addResultToList(self, result):
        """Adds result to the results list, visible in UI.

        Args:
            result: instance of ExperimentResult.
        """
        index = self._results_list.InsertStringItem(sys.maxint,
                                                    result.getDirName())
        self._results_list.SetStringItem(index, 1, result.getAlgorithmName())
        self._results_list.SetStringItem(index, 2, result.getCompressionName())

    def getCheckedIndices(self):
        """Returns a list of indexes (starting from 0):
        which results are checked on the list.
        """
        items_nr = self._results_list.GetItemCount()
        checked_items = []
        for i in xrange(items_nr):
            if self._results_list.IsChecked(i):
                checked_items.append(i)
        return checked_items

    def _selectAllResults(self, select=True):
        """(De)selects all results, depending on 'select' variable.

        Args:
            select: Bool.
        """
        items_nr = self._results_list.GetItemCount()
        for i in xrange(items_nr):
            self._results_list.CheckItem(i, select)

    def _onSelectAll(self, _):
        self._selectAllResults()

    def _onDeselectAll(self, _):
        self._selectAllResults(select=False)

    def _onClickAnalyse(self, _):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(
            self.evt_ANALYSE, self.GetId()))

    def _onClickLoad(self, _):
        choose_file_dialog = wx.FileDialog(self, self._CHOOSE_FILE_TO_LOAD,
                                           "", "", self._FILE_FORMAT,
                                           wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if choose_file_dialog.ShowModal() == wx.ID_CANCEL:
            return
        self._path = choose_file_dialog.GetPath()

        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(
            self.evt_LOAD, self.GetId()))

    def _onClickSave(self, _):
        save_file_dialog = wx.FileDialog(self, self._CHOOSE_FILE_TO_SAVE,
                                         "", self._DEF_FILE_NAME,
                                         self._FILE_FORMAT,
                                         wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if save_file_dialog.ShowModal() == wx.ID_CANCEL:
            return
        self._path = save_file_dialog.GetPath()

        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(
            self.evt_SAVE, self.GetId()))

    def _showError(self, msg):
        wx.MessageBox(msg, "Error", wx.OK | wx.ICON_ERROR)

    def onIncorrectItems(self):
        self._showError(self._INCORRECT_ITEMS)

    def onLoadError(self):
        self._showError(self._CANT_LOAD.format(self._path))

    def onSaveError(self):
        self._showError(self._CANT_SAVE.format(self._path))

    def getPath(self):
        return self._path
