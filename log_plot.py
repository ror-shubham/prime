import wx
import wx.lib.scrolledpanel

import matplotlib
from generic_plot import PlotCanvas

import wx.lib.inspection

matplotlib.use('WXAgg')


class PlotDemoApp(object):
    def __init__(self, data):
        self.app = wx.App()
        plot_titles = list(map(lambda x: "Depth vs " + x, data.columns))
        x_ndarr = data.index.to_numpy()
        y_ndarr = list(map(lambda x: data[x].to_numpy(), data.columns))

        self.frame = PlotCanvas(None, -1, "Log Plot", plot_titles, x_ndarr, y_ndarr, "Depth", list(data.columns.values))
        self.frame.Show(True)
        wx.lib.inspection.InspectionTool().Show()
        self.app.MainLoop()

