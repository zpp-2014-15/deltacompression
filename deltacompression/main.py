"""Module that starts application."""

import sys
import os.path
sys.path.append(os.path.dirname(__file__))

import wx

from deltacompression.gui import controller


def main():
    app = wx.App(False)
    main_controller = controller.MainController(app)
    main_controller.StartApp()
    app.MainLoop()


if __name__ == '__main__':
    main()
