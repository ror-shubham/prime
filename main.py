import wx
from readLas import ReadLas
from log_plot import PlotDemoApp
import numpy as np

import ui


class Frame(ui.MainFrame):
    def __init__(self, parent):
        ui.MainFrame.__init__(self, parent)

    def loadLas(self, event):
        openFileDialog = wx.FileDialog(self, "Open", "", "",
                                       "LAS files (*.las)|*.las",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        path = openFileDialog.GetPath()

        lasObj = ReadLas(path)
        self.df = lasObj.convert_to_df()
        self.df = self.df.replace(-999.2500, np.nan)
        self.ls = ["a", "b", "c"]
        self.log_plot_menu.Enable(True)

    def plot_log( self, event ):
        PlotDemoApp(self.df)

    def add_check_boxes (self, frame):
        ui.MainFrame.m_checkBox4 = wx.CheckBox(self, wx.ID_ANY, u"Check Me---!", wx.DefaultPosition, wx.DefaultSize, 0)
        ui.MainFrame.m_checkBox4.SetValue(True)
        a = ui.MainFrame.GetSizer(frame)
        a.Add(ui.MainFrame.m_checkBox4, 0, wx.ALL, 5)





app = wx.App(False)
frame = Frame(None)
frame.Show(True)
# start the applications
app.MainLoop()
