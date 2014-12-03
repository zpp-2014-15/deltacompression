"""Utils like getting file or directory."""

import wx

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
