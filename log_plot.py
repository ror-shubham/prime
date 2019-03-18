import wx
import matplotlib

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.use('WXAgg')


class PlotDemoApp(object):
    def __init__(self, data):
        self.app = wx.App()
        self.frame = PlotDemoMainFrame(None, -1, "PlotCanvas", data)
        self.frame.Show(True)
        self.app.MainLoop()


class PlotDemoMainFrame(wx.Frame):
    def __init__(self, parent, wxid, title, data):
        wx.Frame.__init__(self, parent, wxid, title,
                          wx.DefaultPosition, (800, 600))

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)

        self.client = FigureCanvas(self, -1, self.figure)

        depth = data.index.to_numpy()
        u = data[data.columns[1]].to_numpy()
        self.axes.plot(u, depth)

        self.client.draw()
