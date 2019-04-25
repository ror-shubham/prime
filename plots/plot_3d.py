import matplotlib as mpl
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

import wx


class Plot(wx.Panel):
    def __init__(self, parent, id=-1, dpi=None, **kwargs):
        wx.Panel.__init__(self, parent, id=id, **kwargs)
        self.figure = mpl.figure.Figure()
        self.canvas = FigureCanvas(parent, -1, self.figure)
        # self.toolbar = NavigationToolbar(self.canvas)
        # self.toolbar.Realize()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        # sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.SetSizer(sizer)


def plot_3d(plotter, data):
    fig = plotter.add_3d('3d cross plot')
    axes = fig.gca(projection='3d')
    data = data.sample(frac=0.01)
    # TODO make the sample taking dynamic based on data size
    x = data.lat
    y = data.long
    z = data.DEPTH
    prop_ind = data.columns[3]
    w = data[prop_ind]
    plt = axes.scatter(x, y, z, c=w, s=30)
    axes.set_xlabel('Latitude')
    axes.set_ylabel('Longitude')
    axes.set_zlabel('Depth')
    cbar = fig.colorbar(plt)
    cbar.set_label(prop_ind)


