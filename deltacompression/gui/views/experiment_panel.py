"""This module contains panel for creating experiments."""

import wx

from deltacompression.gui.views import utils


class ExperimentPanel(wx.Panel):
    """Displays experiment and allows to edit it."""

    evt_ADD_EXPERIMENT = wx.NewEventType()
    EVT_ADD_EXPERIMENT = wx.PyEventBinder(evt_ADD_EXPERIMENT)

    _CHUNKER_PARAMS = "Min chunk: %s, Max chunk: %s, Avg chunk: %s"
    _ADD_EXPERIMENT = "Add Experiment"

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._algorithm_combo_box = None
        self._compression_combo_box = None
        self._dir_picker = None
        self._tests_list = None
        self._chunk_params_label = None
        self._add_test_button = None

        self._initUI()

    def initializeWidgets(self, exp_queue):
        """Sets all widgets to initial values.

        Args:
            experiment_queue: instance of ExperimentQueue.
        """
        self._algorithm_combo_box.Clear()
        self._algorithm_combo_box.AppendItems(
            exp_queue.algorithm_factory.getAlgorithms())
        self._algorithm_combo_box.SetStringSelection(
            exp_queue.def_alg)

        self._compression_combo_box.Clear()
        self._compression_combo_box.AppendItems(
            exp_queue.compression_factory.getCompressions())
        self._compression_combo_box.SetStringSelection(
            exp_queue.def_compr)

        self._tests_list.ClearAll()
        self._tests_list.InsertColumn(0, 'Path')
        self._tests_list.InsertColumn(1, 'Algorithm', width=200)
        self._tests_list.InsertColumn(2, 'Compression', width=150)

        self._chunk_params_label.SetLabel(
            self._CHUNKER_PARAMS % exp_queue.getChunkerParameters()
            .getParameters())

    def updateExperimentsList(self, exp_list):
        self._tests_list.DeleteAllItems()
        for i in range(len(exp_list)):
            self._tests_list.InsertStringItem(i, exp_list[i].getDirName())
            self._tests_list.SetStringItem(
                i, 1, exp_list[i].getAlgorithmName())
            self._tests_list.SetStringItem(
                i, 2, exp_list[i].getCompressionName())
        wx.SafeYield()

    def getSelectedAlgorithm(self):
        return self._algorithm_combo_box.GetStringSelection()

    def getSelectedCompression(self):
        return self._compression_combo_box.GetStringSelection()

    def getSelectedDir(self):
        return self._dir_picker.GetPath()

    def getDirectory(self):
        return utils.getDirectory()

    def _initUI(self):
        """Initializes all controls."""
        vbox = wx.BoxSizer(wx.VERTICAL)

        exp_info_sizer = wx.GridBagSizer(vgap=5, hgap=0)

        text1 = wx.StaticText(self, label="Algorithm")
        text2 = wx.StaticText(self, label="Compression")
        text3 = wx.StaticText(self, label="Directory")
        exp_info_sizer.Add(text1, flag=wx.ALL, border=10,
                           pos=(0, 0), span=(1, 1))
        exp_info_sizer.Add(text2, flag=wx.ALL, border=10,
                           pos=(1, 0), span=(1, 1))
        exp_info_sizer.Add(text3, flag=wx.ALL, border=10,
                           pos=(2, 0), span=(1, 1))

        self._algorithm_combo_box = wx.ComboBox(choices=[], parent=self,
                                                style=wx.CB_READONLY)
        exp_info_sizer.Add(self._algorithm_combo_box, flag=wx.EXPAND,
                           pos=(0, 1), span=(1, 3))

        self._compression_combo_box = wx.ComboBox(choices=[], parent=self,
                                                  style=wx.CB_READONLY)
        exp_info_sizer.Add(self._compression_combo_box, flag=wx.EXPAND,
                           pos=(1, 1), span=(1, 3))

        self._dir_picker = wx.DirPickerCtrl(self)
        exp_info_sizer.Add(self._dir_picker, flag=wx.EXPAND,
                           pos=(2, 1), span=(1, 3))

        self._add_test_button = wx.Button(self, label=self._ADD_EXPERIMENT,
                                          size=(200, -1))
        self._add_test_button.Bind(wx.EVT_BUTTON, self._onClickAddTest)
        exp_info_sizer.Add(self._add_test_button, flag=wx.EXPAND,
                           pos=(0, 4), span=(3, 5))
        exp_info_sizer.AddGrowableCol(2)
        vbox.Add(exp_info_sizer, 0, flag=wx.EXPAND)

        self._tests_list = utils.AutoWidthListCtrl(self)
        vbox.Add(self._tests_list, 1, flag=wx.EXPAND|wx.TOP, border=20)

        self._chunk_params_label = wx.StaticText(self,
                                                 label=self._CHUNKER_PARAMS %
                                                 (None, None, None))
        vbox.Add(self._chunk_params_label, flag=wx.EXPAND)

        self.SetSizer(vbox)

    def _onClickAddTest(self, _):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(
            self.evt_ADD_EXPERIMENT, self.GetId()))
