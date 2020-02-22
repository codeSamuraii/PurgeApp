#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gui.py
© Rémi Héneault (@codesamuraii)
https://github.com/codesamuraii
"""
import wx
import purge_app

class FileDrop(wx.FileDropTarget):
    """Custom drag-and-drop component to launch main functions."""
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def show_error_msgbox(self, message):
        dlg = wx.MessageDialog(self.window, message)
        dlg.ShowModal()

    def OnDropFiles(self, x, y, filenames):
        if len(filenames) > 1:
            self.show_error_msgbox("Please drag a single app at a time.")
            return False

        path_to_app = filenames[0]

        try:
            purge_app.run(path_to_app)
        except Exception as e:
            self.show_error_msgbox(e)
            return False
        else:
            return True


class MainWindow(wx.Frame):
   def __init__(self):
        # Init window components
        wx.Frame.__init__(self, None, title="PurgeApp")
        panel = wx.Panel(self)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create label
        self.label = wx.StaticText(panel, style=wx.ALIGN_CENTER, label="Drag an app to uninstall it")

        # Connect frame to drag-and-drop
        dt = FileDrop(panel)
        panel.SetDropTarget(dt)

        # Center the label
        h_sizer.Add(self.label, 0, wx.CENTER)
        main_sizer.Add((0,0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0,0), 1, wx.EXPAND)
        panel.SetSizer(main_sizer)
        self.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainWindow()
    app.MainLoop()
