import wx
import wx.lib.scrolledpanel

import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.figure import Figure

import wx.lib.inspection

matplotlib.use('WXAgg')


class PlotDemoApp(object):
    def __init__(self, data):
        self.app = wx.App()
        self.frame = PlotCanvas(None, -1, "PlotCanvas", data)
        self.frame.Show(True)
        wx.lib.inspection.InspectionTool().Show()
        self.app.MainLoop()


class PlotCanvas(wx.Frame):
    def __init__(self, parent, wxid, title, data):
        wx.Frame.__init__(self, parent, wxid, title)

        self.box_main = wx.BoxSizer(wx.VERTICAL)
        self.label_dict = {}

        panel_upper = wx.Panel(self)
        box_upper = wx.BoxSizer(wx.HORIZONTAL)
        i = 0
        for column in data.columns:
            cb1 = wx.CheckBox(panel_upper, label=column)
            cb1.SetValue(True)
            box_upper.Add(cb1, 1, wx.EXPAND | wx.LEFT, 15)
            self.Bind(wx.EVT_CHECKBOX, self.on_checked)
            self.label_dict[column] = i
            i += 1
        panel_upper.SetSizer(box_upper)
        self.box_main.Add(panel_upper)

        panel_lower = wx.lib.scrolledpanel.ScrolledPanel(self, size=(2500,-1))
        panel_lower.SetupScrolling()
        panel_lower.SetBackgroundColour("White")
        self.box_lower = wx.BoxSizer(wx.HORIZONTAL)

        box_local = wx.BoxSizer(wx.VERTICAL)
        plt = Figure(figsize=(95,10))
        num_columns = len(data.columns)
        axes_1 = plt.add_subplot(1, num_columns, 1)
        data_numpy = data[data.columns[0]].to_numpy()
        depth = data.index.to_numpy()
        plt.gca().invert_yaxis()
        plt.subplots_adjust(left=0.01, right=1.00, top=0.95, bottom=0.05)
        axes_1.plot(data_numpy, depth)
        for i in range(1, num_columns):
            axes_tmp = plt.add_subplot(1, num_columns, i+1, sharey=axes_1)
            axes_tmp.set(xlabel=data.columns[i], ylabel='Depth', title='Depth vs ' + data.columns[i])

            data_numpy = data[data.columns[i]].to_numpy()

            plt.gca().invert_yaxis()
            axes_tmp.plot(data_numpy, depth)
        canvas = FigureCanvas(panel_lower, -1, plt)
        canvas.draw()
        box_local.Add(canvas, 1, wx.EXPAND)
        panel_nav = wx.Panel(self)
        box_nav = wx.BoxSizer(wx.HORIZONTAL)
        toolbar = NavigationToolbar(canvas)
        box_nav.Add(toolbar)
        panel_nav.SetSizer(box_nav)
        toolbar.Realize()
        self.box_main.Add(panel_nav, 0, wx.CENTER)
        self.box_lower.Add(box_local, 1, wx.EXPAND)

        self.box_main.Add(panel_lower, 1, wx.EXPAND)
        panel_lower.SetSizer(self.box_lower)
        self.SetSizer(self.box_main)
        self.box_main.Layout()
        self.Maximize(True)

    def on_checked(self, e):
        cb = e.GetEventObject()
        index = self.label_dict[cb.GetLabel()]
        if not cb.GetValue():
            self.box_lower.Hide(index)
            self.box_main.Layout()
            self.Fit()
        else:
            self.box_lower.Show(index)
            self.box_main.Layout()
            self.Fit()

