"""This module contains panel for creating experiments."""

import wx

from deltacompression.gui.views import utils


class ExperimentPanel(wx.Panel):
    """Displays experiment and allows to edit it."""

    evt_ALGORITHM_SELECTED = wx.NewEventType()
    EVT_ALGORITHM_SELECTED = wx.PyEventBinder(evt_ALGORITHM_SELECTED)

    evt_COMPRESSION_SELECTED = wx.NewEventType()
    EVT_COMPRESSION_SELECTED = wx.PyEventBinder(evt_COMPRESSION_SELECTED)

    evt_ADD_TEST = wx.NewEventType()
    EVT_ADD_TEST = wx.PyEventBinder(evt_ADD_TEST)

    evt_REMOVE_TEST = wx.NewEventType()
    EVT_REMOVE_TEST = wx.PyEventBinder(evt_REMOVE_TEST)

    evt_SIMULATE = wx.NewEventType()
    EVT_SIMULATE = wx.PyEventBinder(evt_SIMULATE)

    evt_TEST_SELECTED = wx.NewEventType()
    EVT_TEST_SELECTED = wx.PyEventBinder(evt_TEST_SELECTED)

    _CHUNKER_PARAMS = "Min chunk: %s, Max chunk: %s, Avg chunk: %s"
    _ADD_TEST = "Add test"
    _REMOVE_TEST = "Remove test"
    _SIMULATE = "Simulate"

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._algorithm_combo_box = None
        self._compression_combo_box = None
        self._tests_list_box = None
        self._chunk_params_label = None
        self._add_test_button = None
        self._remove_test_button = None
        self._simulate_button = None

        self._initUI()

    def initializeExperiment(self, experiment):
        """Sets all widgets to initial values.

        Args:
            experiment: instance of Experiment.
        """
        self._algorithm_combo_box.Clear()
        self._algorithm_combo_box.AppendItems(
            experiment.algorithm_factory.getAlgorithms())
        self._algorithm_combo_box.SetStringSelection(
            experiment.def_alg)
        self._algorithm_combo_box.Disable()

        self._compression_combo_box.Clear()
        self._compression_combo_box.AppendItems(
            experiment.compression_factory.getCompressions())
        self._compression_combo_box.SetStringSelection(
            experiment.def_compr)
        self._compression_combo_box.Disable()

        self._tests_list_box.Clear()

        self._chunk_params_label.SetLabel(
            self._CHUNKER_PARAMS % experiment.getChunkerParams()
            .getParameters())

    def updateAlgorithm(self, experiment):
        """Updates information about algorithm of a currently selected test

        Args:
            experiment: instance of Experiment.
        """
        selected_test_nr = self.getSelectedTest()
        if selected_test_nr >= 0:
            test = experiment.getTest(selected_test_nr)
            self._algorithm_combo_box.SetStringSelection(
                test.getAlgorithmName())
            self._algorithm_combo_box.Enable()
        else:
            self._algorithm_combo_box.SetStringSelection(
                experiment.def_alg)
            self._algorithm_combo_box.Disable()

    def updateCompression(self, experiment):
        """Updates information about compression of a currently selected test

        Args:
            experiment: instance of Experiment.
        """
        selected_test_nr = self.getSelectedTest()
        if selected_test_nr >= 0:
            test = experiment.getTest(selected_test_nr)
            self._compression_combo_box.SetStringSelection(
                test.getCompressionName())
            self._compression_combo_box.Enable()
        else:
            self._compression_combo_box.SetStringSelection(
                experiment.def_compr)
            self._compression_combo_box.Disable()

    def addTestToList(self, test):
        self._tests_list_box.Append(test.getDirName())

    def removeTestFromList(self, test_nr):
        self._tests_list_box.Delete(test_nr)

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
        self._algorithm_combo_box.Bind(wx.EVT_COMBOBOX, self._onSelectAlgorithm)
        sizer.Add(self._algorithm_combo_box, flag=wx.EXPAND)

        self._compression_combo_box = wx.ComboBox(choices=[], parent=self)
        self._compression_combo_box.Bind(wx.EVT_COMBOBOX,
                                         self._onSelectCompression)
        sizer.Add(self._compression_combo_box, flag=wx.EXPAND)

        self._tests_list_box = wx.ListBox(parent=self)
        self._tests_list_box.Bind(wx.EVT_LISTBOX, self._onTestSelected)
        sizer.Add(self._tests_list_box, flag=wx.EXPAND)

        self._add_test_button = wx.Button(self, label=self._ADD_TEST)
        sizer.Add(self._add_test_button, flag=wx.EXPAND)
        self._add_test_button.Bind(wx.EVT_BUTTON, self._onClickAddTest)

        self._remove_test_button = wx.Button(self, label=self._REMOVE_TEST)
        sizer.Add(self._remove_test_button, flag=wx.EXPAND)
        self._remove_test_button.Bind(wx.EVT_BUTTON, self._onClickRemoveTest)

        self._chunk_params_label = wx.StaticText(self,
                                                 label=self._CHUNKER_PARAMS %
                                                 (None, None, None))
        sizer.Add(self._chunk_params_label, flag=wx.EXPAND)

        self._simulate_button = wx.Button(self, label=self._SIMULATE)
        sizer.Add(self._simulate_button, flag=wx.EXPAND)
        self._simulate_button.Bind(wx.EVT_BUTTON, self._onClickSimulate)

        self.SetSizer(sizer)

    def _onSelectAlgorithm(self, _):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(
            self.evt_ALGORITHM_SELECTED, self.GetId()))

    def _onSelectCompression(self, _):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(
            self.evt_COMPRESSION_SELECTED, self.GetId()))

    def _onClickAddTest(self, _):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(
            self.evt_ADD_TEST, self.GetId()))

    def _onClickRemoveTest(self, _):
        if self.getSelectedTest() != -1:
            # a test is selected
            self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(
                self.evt_REMOVE_TEST, self.GetId()))

    def _onClickSimulate(self, _):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(
            self.evt_SIMULATE, self.GetId()))

    def _onTestSelected(self, _):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(
            self.evt_TEST_SELECTED, self.GetId()))
