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

    _ANALYSE = 'Analyse'
    _SELECT_ALL = 'Select all'
    _DESELECT_ALL = 'Deselect all'

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._results_list = None
        self._select_all_button = None
        self._deselect_all_button = None
        self._analyse_button = None

        self._initUI()

    def _initUI(self):
        """Initializes all controls."""
        sizer = wx.BoxSizer(wx.VERTICAL)

        self._results_list = utils.CheckListCtrl(self)
        self._results_list.InsertColumn(0, 'Path')
        self._results_list.InsertColumn(1, 'Algorithm', width=200)
        self._results_list.InsertColumn(2, 'Compression', width=150)
        sizer.Add(self._results_list, 1, wx.EXPAND)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self._select_all_button = wx.Button(self, label=self._SELECT_ALL)
        self._select_all_button.Bind(wx.EVT_BUTTON, self._onSelectAll)

        self._deselect_all_button = wx.Button(self, label=self._DESELECT_ALL)
        self._deselect_all_button.Bind(wx.EVT_BUTTON, self._onDeselectAll)

        hbox.Add(self._select_all_button, 1, wx.EXPAND)
        hbox.Add(self._deselect_all_button, 1, wx.EXPAND)
        sizer.Add(hbox, 0, wx.EXPAND)

        self._analyse_button = wx.Button(self, label=self._ANALYSE,
                                         size=(-1, 50))
        self._analyse_button.Bind(wx.EVT_BUTTON, self._onClickAnalyse)
        sizer.Add(self._analyse_button, 0, wx.EXPAND)

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

    def getCheckedResults(self):
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
