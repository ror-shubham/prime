import numpy as np

import wx
import wx.xrc
import wx.lib.scrolledpanel

import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.figure import Figure

import wx.lib.inspection

matplotlib.use('WXAgg')


class GenericPlot(object):
    def __init__(self, frame_title, plot_titles, x_ndarr, y_ndarr, x_labels, y_labels):
        self.app = wx.App()
        self.frame = PlotCanvas(None, -1, frame_title,  plot_titles, x_ndarr, y_ndarr, x_labels, y_labels)
        self.frame.Show(True)
        wx.lib.inspection.InspectionTool().Show()
        self.app.MainLoop()


class PlotCanvas(wx.Frame):
    def __init__(self, parent, wxid, frame_title, plot_titles, x_ndarr, y_ndarr, x_labels, y_labels):
        # x_ndarr = array of x_data or 1d array if x axis is common
        # y_ndarr = array of y_data
        # x_labels = list of x_labels or a single string if common
        # y_labels = list of y_labels or a single string if common
        a = x_ndarr
        b = np.asarray(x_ndarr)
        c = b.ndim
        is_xaxis_common = not(isinstance(x_ndarr[0], list) or isinstance(x_ndarr[0], np.ndarray))
        is_ylabel_common = not isinstance(y_labels, list)
        is_xlabel_common = not isinstance(x_labels, list)

        wx.Frame.__init__(self, parent, wxid, frame_title)

        self.box_main = wx.BoxSizer(wx.VERTICAL)

        self.label_dict = {}
        #
        #         panel_upper = wx.Panel(self)
        #         box_upper = wx.BoxSizer(wx.HORIZONTAL)
        #         i = 0
        #         for column in data.columns:
        #             cb1 = wx.CheckBox(panel_upper, label=column)
        #             cb1.SetValue(True)
        #             box_upper.Add(cb1, 1, wx.EXPAND | wx.LEFT, 15)
        #             self.Bind(wx.EVT_CHECKBOX, self.on_checked)
        #             self.label_dict[column] = i
        #             i += 1
        #         panel_upper.SetSizer(box_upper)
        #         self.box_main.Add(panel_upper)

        panel_lower = wx.lib.scrolledpanel.ScrolledPanel(self)
        panel_lower.SetupScrolling()
        panel_lower.SetBackgroundColour("White")
        self.box_lower = wx.BoxSizer(wx.HORIZONTAL)

        box_local = wx.BoxSizer(wx.VERTICAL)
        num_columns = len(y_ndarr)
        fig_width = 6 * num_columns     # one subplot takes 6 inches
        plt = Figure(figsize=(fig_width, 10))

        axes_1 = plt.add_subplot(1, num_columns, 1)
        x_label_here = x_labels if is_xlabel_common else x_labels[0]
        y_label_here = y_labels if is_ylabel_common else y_labels[0]
        x_axis_data_here = x_ndarr if is_xaxis_common else x_ndarr[0]
        axes_1.set(xlabel=x_label_here, ylabel=y_label_here, title=plot_titles[0])
        plt.gca().invert_yaxis()
        plt.subplots_adjust(left=0.01+0.05/num_columns, right=0.99-(0.01/num_columns), top=0.94, bottom=0.05)
        axes_1.plot(y_ndarr[0], x_axis_data_here)
        for i in range(1, num_columns):
            x_label_here = x_labels if is_xlabel_common else x_labels[i]
            y_label_here = y_labels if is_ylabel_common else y_labels[i]
            x_ndarr_here = x_ndarr if is_xaxis_common else x_ndarr[i]
            axes_tmp = plt.add_subplot(1, num_columns, i+1, sharey=axes_1)
            axes_tmp.set(xlabel=x_label_here, ylabel=y_label_here, title=plot_titles[i])
            axes_tmp.plot(y_ndarr[i], x_ndarr_here)
        canvas = FigureCanvas(panel_lower, -1, plt)
        canvas.draw()
        box_local.Add(canvas, 1, wx.EXPAND)
        panel_nav = wx.Panel(self)
        box_nav = wx.BoxSizer(wx.HORIZONTAL)
        toolbar = NavigationToolbar(canvas)
        box_nav.Add(toolbar)
        panel_nav.SetSizer(box_nav)
        toolbar.Realize()
        self.box_main.Add(box_nav, 0, wx.CENTER)
        self.box_lower.Add(box_local, 1, wx.EXPAND)

        self.box_main.Add(panel_lower, 1, wx.EXPAND)
        panel_lower.SetSizer(self.box_lower)
        self.SetSizer(self.box_main)
        self.box_main.Layout()
        self.Maximize(True)

    # def on_checked(self, e):
    #         cb = e.GetEventObject()
    #         index = self.label_dict[cb.GetLabel()]
    #         if not cb.GetValue():
    #             self.box_lower.Hide(index)
    #             self.box_main.Layout()
    #             self.Fit()
    #         else:
    #             self.box_lower.Show(index)
    #             self.box_main.Layout()
    #             self.Fit()

