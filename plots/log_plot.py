import wx
import wx.lib.scrolledpanel

import matplotlib
from plots.generic_plot import PlotCanvas

matplotlib.use('WXAgg')


class PlotLog(object):
    def __init__(self, parent, plotter, data):
        plot_titles = list(map(lambda x: "Depth vs " + x, data.columns))
        x_ndarr = data.index.to_numpy()
        y_ndarr = list(map(lambda x: data[x].to_numpy(), data.columns))

        pnl = PlotCanvas(parent, plot_titles, x_ndarr, y_ndarr, "Depth", list(data.columns.values))
        plotter.nb.AddPage(pnl, "Log plot")
        parent.Layout()
