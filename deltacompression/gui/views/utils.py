"""Utils like getting file or directory."""

import wx

from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin


_DIRECTORY_TO_CHOOSE = "Choose a directory"
_FILE_TO_CHOOSE = "Choose a file"


def _getDataFromDialog(dialog):
    if dialog.ShowModal() == wx.ID_OK:
        result = dialog.GetPath()
    else:
        result = ""

    dialog.Destroy()
    return result

def getDirectory():
    """Allows user to choose directory.
    Returns:
        Absolute path or empty string if user canceled dialog.
    """
    dialog = wx.DirDialog(None, _DIRECTORY_TO_CHOOSE, style=wx.DD_DEFAULT_STYLE)
    return _getDataFromDialog(dialog)

def getFilePath():
    """Allows user to choose file.
    Returns:
        Absolute path to file or empty string if user canceled dialog.
    """
    dialog = wx.FileDialog(None, _FILE_TO_CHOOSE, style=wx.DD_DEFAULT_STYLE)
    return _getDataFromDialog(dialog)


class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    """Mixin list class used in multiple panels. It automatically
    resizes the first column to take extra space after resizing."""

    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(0)


class CheckListCtrl(AutoWidthListCtrl, CheckListCtrlMixin):
    """Mixin list class used in multiple panels.
    It's like AutoWidthListCtrl where you can check list items."""
    def __init__(self, parent):
        AutoWidthListCtrl.__init__(self, parent)
        CheckListCtrlMixin.__init__(self)
