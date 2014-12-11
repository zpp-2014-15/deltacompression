"""Module that starts application."""

import sys
import os.path
sys.path.append(os.path.dirname(__file__))

import wx

from deltacompression.gui.controllers import main_controller


def main():
    app = wx.App(False)
    con = main_controller.MainController(app)
    con.startApp()
    app.MainLoop()


if __name__ == '__main__':
    main()
