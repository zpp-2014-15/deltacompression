"""This module contains panel for creating experiments."""

import wx

from deltacompression.gui.models import experiment
from deltacompression.gui.views import utils


class ExperimentPanel(wx.Panel):
    """Displays experiment and allows to edit it.

    Attributes:
        evt_ADD_EXPERIMENT: event meaning that a new experiment was added.
        EVT_ADD_EXPERIMENT: evt_ADD_EXPERIMENT's binder.

        _CHUNKER_PARAMS: String, text displaying chunker params.
        _ADD_EXPERIMENT: String, name of add_experiment_button.
    """

    evt_ADD_EXPERIMENT = wx.NewEventType()
    EVT_ADD_EXPERIMENT = wx.PyEventBinder(evt_ADD_EXPERIMENT)

    _CHUNKER_PARAMS = "Min chunk: %s, Max chunk: %s, Avg chunk: %s"
    _ADD_EXPERIMENT = "Add Experiment"

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._algorithm_combo_box = None
        self._compression_combo_box = None
        self._dir_picker = None
        self._experiments_list = None
        self._chunk_params_label = None
        self._add_experiment_button = None

        self._initUI()

    def _updateWidgets(self):
        """Sets all widgets to proper values (sets choices correctly, etc.)."""

        self._algorithm_combo_box.AppendItems(
            experiment.Experiment.alg_factory.getAlgorithms())
        self._algorithm_combo_box.SetStringSelection(
            experiment.Experiment.def_alg)

        self._compression_combo_box.AppendItems(
            experiment.Experiment.compr_factory.getCompressions())
        self._compression_combo_box.SetStringSelection(
            experiment.Experiment.def_compr)

        self._experiments_list.InsertColumn(0, 'Path')
        self._experiments_list.InsertColumn(1, 'Algorithm', width=200)
        self._experiments_list.InsertColumn(2, 'Compression', width=150)

        # assumption that chunker parameters of all experiments are the same
        # might change in the future
        self._chunk_params_label.SetLabel(
            self._CHUNKER_PARAMS % experiment.Experiment.chunker_params
            .getParameters())

    def updateExperimentsList(self, exp_list):
        """Repaints the experiments list.

        Args:
            exp_list: list of Experiment object.
        """
        self._experiments_list.DeleteAllItems()
        for idx, exp in enumerate(exp_list):
            self._experiments_list.InsertStringItem(idx, exp.getDirName())
            self._experiments_list.SetStringItem(
                idx, 1, exp.getAlgorithmName())
            self._experiments_list.SetStringItem(
                idx, 2, exp.getCompressionName())
        # 'Refreshes' main loop, so that repainting view is done before
        # other long events, like e.g. running an experiment.
        # When we implement running experiments in the background, it
        # probably won't be needed.
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
        """Creates all controls."""
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

        self._add_experiment_button = wx.Button(self,
                                                label=self._ADD_EXPERIMENT,
                                                size=(200, -1))
        self._add_experiment_button.Bind(wx.EVT_BUTTON,
                                         self._onClickAddExperiment)
        exp_info_sizer.Add(self._add_experiment_button, flag=wx.EXPAND,
                           pos=(0, 4), span=(3, 5))
        exp_info_sizer.AddGrowableCol(2)
        vbox.Add(exp_info_sizer, 0, flag=wx.EXPAND)

        self._experiments_list = utils.AutoWidthListCtrl(self)
        vbox.Add(self._experiments_list, 1, flag=wx.EXPAND|wx.TOP, border=20)

        self._chunk_params_label = wx.StaticText(self,
                                                 label=self._CHUNKER_PARAMS %
                                                 (None, None, None))
        vbox.Add(self._chunk_params_label, flag=wx.EXPAND)

        self.SetSizer(vbox)

        self._updateWidgets()

    def _onClickAddExperiment(self, _):
        self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(
            self.evt_ADD_EXPERIMENT, self.GetId()))
