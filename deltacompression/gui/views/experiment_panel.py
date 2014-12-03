"""This module contains panel for creating experiments."""

import wx


class ExperimentPanel(wx.Panel):

    evt_ALGORITHM_SELECTED = wx.NewEventType()
    EVT_ALGORITHM_SELECTED = wx.PyEventBinder(evt_ALGORITHM_SELECTED)

    _MIN_MAX_CHUNK = "Min chunk: %s, Max chunk: %s"

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self._initUI()

    def updateExperiment(self, experiment):
        self._setPossibleAlgorithms(
            experiment.algorithm_factory.getAlgorithms())
        # TODO: Add factory for compression - just like for algorithms
        self._setPossibleCompressions(["None"])
        self._algorithm_combo_box.SetStringSelection(
            experiment.getAlgorithmName())

        self._compression_combo_box.SetStringSelection(
            experiment.getCompressionName())
        self._min_max_chunk_label.SetLabel(self._MIN_MAX_CHUNK %
                                           experiment.getChunkSizeRange())

    def _initUI(self):
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

        self._min_max_chunk_label = wx.StaticText(self,
                                                  label=self._MIN_MAX_CHUNK %
                                                  (None, None))
        sizer.Add(self._min_max_chunk_label, 0, wx.EXPAND | wx.ALL)

        self.SetSizer(sizer)

    def _setPossibleAlgorithms(self, algorithms):
        self._algorithm_combo_box.Clear()
        for algorithm in algorithms:
            self._algorithm_combo_box.Append(algorithm)

    def _setPossibleCompressions(self, compressions):
        self._compression_combo_box.Clear()
        for compression in compressions:
            self._compression_combo_box.Append(compression)

    def _onSelectAlgorithm(self, _):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(
            self.EVT_ALGORITHM_SELECTED, self.GetId()))
        print self._algorithm_combo_box.GetStringSelection()

    def _onSelectCompression(self, _):
        print self._compression_combo_box.GetStringSelection()
