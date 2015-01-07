"""This module contains panel for creating experiments."""

import wx
import sys

from deltacompression.gui.views import utils


class ExperimentsPanel(wx.Panel):
    """Displays experiment and allows to edit it."""

    evt_ADD_TEST = wx.NewEventType()
    EVT_ADD_TEST = wx.PyEventBinder(evt_ADD_TEST)

    evt_SIMULATE = wx.NewEventType()
    EVT_SIMULATE = wx.PyEventBinder(evt_SIMULATE)

    _CHUNKER_PARAMS = "Min chunk: %s, Max chunk: %s, Avg chunk: %s"
    _ADD_TEST = "Add test"
    _SIMULATE = "Simulate"

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._algorithm_combo_box = None
        self._compression_combo_box = None
        self._tests_list = None
        self._chunk_params_label = None
        self._add_test_button = None
        self._simulate_button = None

        self._initUI()

    def initializeWidgets(self, experiment_set):
        """Sets all widgets to initial values.

        Args:
            experiment: instance of Experiment.
        """
        self._algorithm_combo_box.Clear()
        self._algorithm_combo_box.AppendItems(
            experiment_set.algorithm_factory.getAlgorithms())
        self._algorithm_combo_box.SetStringSelection(
            experiment_set.def_alg)

        self._compression_combo_box.Clear()
        self._compression_combo_box.AppendItems(
            experiment_set.compression_factory.getCompressions())
        self._compression_combo_box.SetStringSelection(
            experiment_set.def_compr)

        self._tests_list.ClearAll()
        self._tests_list.InsertColumn(0, 'Path', width=200)
        self._tests_list.InsertColumn(1, 'Algorithm', width=100)
        self._tests_list.InsertColumn(2, 'Compression', width=100)

        self._chunk_params_label.SetLabel(
            self._CHUNKER_PARAMS % experiment_set.getChunkerParameters()
            .getParameters())

    def addExperimentToList(self, experiment):
        # wywalic sys i jakos ladniej niz 0 1 2 zrobic
        index = self._tests_list.InsertStringItem(sys.maxint, experiment.getDirName())
        self._tests_list.SetStringItem(index, 1, experiment.getAlgorithmName())
        self._tests_list.SetStringItem(index, 2, experiment.getCompressionName())

    def removeExperimentFromList(self, index):
        self._tests_list.DeleteItem(index)

    def getSelectedAlgorithm(self):
        return self._algorithm_combo_box.GetStringSelection()

    def getSelectedCompression(self):
        return self._compression_combo_box.GetStringSelection()

    def getSelectedTest(self):
        return self._tests_list_box.GetSelection()

    def getDirectory(self):
        return utils.getDirectory()

    def _initUI(self):
        """Initialize all controls."""
        sizer = wx.BoxSizer(wx.VERTICAL)

        self._algorithm_combo_box = wx.ComboBox(choices=[], parent=self)
        sizer.Add(self._algorithm_combo_box, flag=wx.EXPAND)

        self._compression_combo_box = wx.ComboBox(choices=[], parent=self)
        sizer.Add(self._compression_combo_box, flag=wx.EXPAND)

        self._add_test_button = wx.Button(self, label=self._ADD_TEST)
        self._add_test_button.Bind(wx.EVT_BUTTON, self._onClickAddTest)
        sizer.Add(self._add_test_button, flag=wx.EXPAND)

        self._tests_list = wx.ListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN) # check styles
        sizer.Add(self._tests_list, 1, flag=wx.EXPAND)

        self._chunk_params_label = wx.StaticText(self,
                                                 label=self._CHUNKER_PARAMS %
                                                 (None, None, None))
        sizer.Add(self._chunk_params_label, flag=wx.EXPAND)

        self._simulate_button = wx.Button(self, label=self._SIMULATE)
        sizer.Add(self._simulate_button, flag=wx.EXPAND)
        self._simulate_button.Bind(wx.EVT_BUTTON, self._onClickSimulate)

        self.SetSizer(sizer)

    def _onClickAddTest(self, _):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(
            self.evt_ADD_TEST, self.GetId()))

    def _onClickSimulate(self, _):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(
            self.evt_SIMULATE, self.GetId()))
