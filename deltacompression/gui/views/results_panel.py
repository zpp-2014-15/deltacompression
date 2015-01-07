import wx
import sys

from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin


class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):

    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)


# dodac jakies select all, deselect etc.
class ResultsPanel(wx.Panel):
    
    _ANALYSE = 'Analyse'
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._results_list = None
        self._analyse_button = None

        self._initUI()

    def _initUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        self._results_list = CheckListCtrl(self)
        self._results_list.InsertColumn(0, 'Path', width=200)
        self._results_list.InsertColumn(1, 'Algorithm', width=100)
        self._results_list.InsertColumn(2, 'Compression', width=100)
        sizer.Add(self._results_list, 1, wx.EXPAND)

        self._analyse_button = wx.Button(self, label=self._ANALYSE)
        sizer.Add(self._analyse_button, 1, wx.EXPAND)
        # polaczyc button z eventem

        self.SetSizer(sizer)

    def addResultToList(self, result):
        index = self._results_list.InsertStringItem(sys.maxint, result.getDirName())
        self._results_list.SetStringItem(index, 1, result.getAlgorithmName())
        self._results_list.SetStringItem(index, 2, result.getCompressionName())
