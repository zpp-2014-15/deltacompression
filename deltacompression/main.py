"""Module that starts application."""

import sys
import os.path
sys.path.append(os.path.dirname(__file__))

import wx

from deltacompression.gui import controller


def main():
    app = wx.App(False)
    controller.MainController(app)
    app.MainLoop()


if __name__ == '__main__':
    main()
