"""This module contains panel for creating experiments."""

import wx

from deltacompression.gui.views import utils


class ExperimentPanel(wx.Panel):
    """Displays experiment and allows to edit it."""

    evt_ALGORITHM_SELECTED = wx.NewEventType()
    EVT_ALGORITHM_SELECTED = wx.PyEventBinder(evt_ALGORITHM_SELECTED)

    evt_ADD_FILE = wx.NewEventType()
    EVT_ADD_FILE = wx.PyEventBinder(evt_ADD_FILE)

    evt_SIMULATE = wx.NewEventType()
    EVT_SIMULATE = wx.PyEventBinder(evt_SIMULATE)

    _MIN_MAX_CHUNK = "Min chunk: %s, Max chunk: %s"
    _ADD_FILE = "Add file"
    _SIMULATE = "Simulate"

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._compression_combo_box = None
        self._add_file_button = None
        self._min_max_chunk_label = None
        self._file_list_box = None
        self._algorithm_combo_box = None

        self._initUI()

    def updateExperiment(self, experiment):
        """Updates information associated with experiment.

        Args:
            experiment: instance of Experiment.
        """
        self._algorithm_combo_box.Clear()
        self._algorithm_combo_box.AppendItems(
            experiment.algorithm_factory.getAlgorithms())
        # TODO: Add factory for compression - just like for algorithms
        self._compression_combo_box.Clear()
        self._compression_combo_box.AppendItems(["None"])

        self._algorithm_combo_box.SetStringSelection(
            experiment.getAlgorithmName())

        self._compression_combo_box.SetStringSelection(
            experiment.getCompressionName())

        self._file_list_box.Clear()
        self._file_list_box.AppendItems(experiment.getFileList())


        self._min_max_chunk_label.SetLabel(self._MIN_MAX_CHUNK %
                                           experiment.getChunkSizeRange())

    def getSelectedAlgorithm(self):
        return self._algorithm_combo_box.GetStringSelection()

    def getFile(self):
        return utils.getFilePath()

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

        self._file_list_box = wx.ListBox(parent=self)
        sizer.Add(self._file_list_box, 0, wx.EXPAND | wx.ALL)

        self._add_file_button = wx.Button(self, label=self._ADD_FILE)
        sizer.Add(self._add_file_button, 0, wx.EXPAND | wx.ALL)
        self._add_file_button.Bind(wx.EVT_BUTTON, self._addFileClicked)

        self._min_max_chunk_label = wx.StaticText(self,
                                                  label=self._MIN_MAX_CHUNK %
                                                  (None, None))
        sizer.Add(self._min_max_chunk_label, 0, wx.EXPAND | wx.ALL)

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

    def _addFileClicked(self, _):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(
            self.evt_ADD_FILE, self.GetId()))

    def _onSelectCompression(self, _):
        print self._compression_combo_box.GetStringSelection()
