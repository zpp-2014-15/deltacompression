"""This module contains panel for creating experiments."""

import wx

from deltacompression.gui.views import utils


class ExperimentPanel(wx.Panel):
    """Displays experiment and allows to edit it."""

    evt_ALGORITHM_SELECTED = wx.NewEventType()
    EVT_ALGORITHM_SELECTED = wx.PyEventBinder(evt_ALGORITHM_SELECTED)

    evt_COMPRESSION_SELECTED = wx.NewEventType()
    EVT_COMPRESSION_SELECTED = wx.PyEventBinder(evt_COMPRESSION_SELECTED)

    evt_CHOOSE_DATA = wx.NewEventType()
    EVT_CHOOSE_DATA = wx.PyEventBinder(evt_CHOOSE_DATA)

    evt_SIMULATE = wx.NewEventType()
    EVT_SIMULATE = wx.PyEventBinder(evt_SIMULATE)

    _CHUNKER_PARAMS = "Min chunk: %s, Max chunk: %s, Avg chunk: %s"
    _CHOOSE_DATA = "Choose data"
    _SIMULATE = "Simulate"

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._algorithm_combo_box = None
        self._compression_combo_box = None
        self._versions_list_box = None
        self._chunk_params_label = None
        self._choose_data_button = None
        self._simulate_button = None

        self._initUI()

    def updateExperiment(self, experiment):
        """Updates information associated with experiment.

        Args:
            experiment: instance of Experiment.
        """
        self._algorithm_combo_box.Clear()
        self._algorithm_combo_box.AppendItems(
            experiment.algorithm_factory.getAlgorithms())

        self._compression_combo_box.Clear()
        self._compression_combo_box.AppendItems(
            experiment.compression_factory.getCompressions())

        self._algorithm_combo_box.SetStringSelection(
            experiment.getAlgorithmName())

        self._compression_combo_box.SetStringSelection(
            experiment.getCompressionName())

        self._versions_list_box.Clear()
        self._versions_list_box.AppendItems(experiment.getVersionsList())


        self._chunk_params_label.SetLabel(
            self._CHUNKER_PARAMS % experiment.getChunkerParameters()
            .getParameters())

    def getSelectedAlgorithm(self):
        return self._algorithm_combo_box.GetStringSelection()

    def getSelectedCompression(self):
        return self._compression_combo_box.GetStringSelection()

    def getFile(self):
        return utils.getFilePath()

    def getDirectory(self):
        return utils.getDirectory()

    def _initUI(self):
        """Initialize all controls."""
        sizer = wx.BoxSizer(wx.VERTICAL)

        self._algorithm_combo_box = wx.ComboBox(choices=[], parent=self)
        self._algorithm_combo_box.Bind(wx.EVT_COMBOBOX, self._onSelectAlgorithm)
        sizer.Add(self._algorithm_combo_box, 0, wx.EXPAND | wx.ALL)

        self._compression_combo_box = wx.ComboBox(choices=[], parent=self)
        self._compression_combo_box.Bind(wx.EVT_COMBOBOX,
                                         self._onSelectCompression)
        sizer.Add(self._compression_combo_box, 0, wx.EXPAND | wx.ALL)

        self._versions_list_box = wx.ListBox(parent=self)
        sizer.Add(self._versions_list_box, 0, wx.EXPAND | wx.ALL)

        self._choose_data_button = wx.Button(self, label=self._CHOOSE_DATA)
        sizer.Add(self._choose_data_button, 0, wx.EXPAND | wx.ALL)
        self._choose_data_button.Bind(wx.EVT_BUTTON, self._chooseDataClicked)

        self._chunk_params_label = wx.StaticText(self,
                                                 label=self._CHUNKER_PARAMS %
                                                 (None, None, None))
        sizer.Add(self._chunk_params_label, 0, wx.EXPAND | wx.ALL)

        self._simulate_button = wx.Button(self, label=self._SIMULATE)
        sizer.Add(self._simulate_button, 0, wx.EXPAND | wx.ALL)
        self._simulate_button.Bind(wx.EVT_BUTTON, self._simulateClicked)

        self.SetSizer(sizer)

    def _simulateClicked(self, _):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(
            self.evt_SIMULATE, self.GetId()))

    def _onSelectAlgorithm(self, _):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(
            self.evt_ALGORITHM_SELECTED, self.GetId()))

    def _chooseDataClicked(self, _):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(
            self.evt_CHOOSE_DATA, self.GetId()))

    def _onSelectCompression(self, _):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(
            self.evt_COMPRESSION_SELECTED, self.GetId()))
