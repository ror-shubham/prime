import wx
import wx.xrc
import wx.lib.scrolledpanel

import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.figure import Figure

import wx.lib.inspection

matplotlib.use('WXAgg')


class SelectCrossPlotField(wx.Dialog):
    def __init__(self, parent, choices):
        wx.Dialog.__init__(self, parent, title="Select Field to cross plot")

        box_main = wx.BoxSizer(wx.VERTICAL)
        box_well_id = wx.BoxSizer(wx.VERTICAL)

        self.static_well = wx.StaticText(self, wx.ID_ANY, u"Field: ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_well.Wrap(-1)

        box_well_id.Add(self.static_well, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.choice_box = wx.Choice(self, choices=choices)
        box_well_id.Add(self.choice_box, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        self.choice_box.SetSelection(0)

        box_main.Add(box_well_id, 1, wx.EXPAND, 5)

        box_buttons = wx.StdDialogButtonSizer()
        self.btn_ok = wx.Button(self, wx.ID_OK)
        box_buttons.AddButton(self.btn_ok)
        self.btn_cancel = wx.Button(self, wx.ID_CANCEL)
        box_buttons.AddButton(self.btn_cancel)
        box_buttons.Realize()

        box_main.Add(box_buttons, 1, wx.EXPAND, 5)

        self.SetSizer(box_main)
        self.Layout()
        box_main.Fit(self)

        self.Centre(wx.BOTH)

    def get_selection(self):
        return self.choice_box.GetStringSelection()


class PlotCross(object):
    def __init__(self, df_arr, df_field):
        self.app = wx.App()
        self.frame = PlotCanvas(None, -1, "Cross Plot", df_arr, df_field)
        self.frame.Show(True)
        wx.lib.inspection.InspectionTool().Show()
        self.app.MainLoop()


class PlotCanvas(wx.Frame):
    def __init__(self, parent, wxid, title, df_arr, df_field):
        wx.Frame.__init__(self, parent, wxid, title)

        self.box_main = wx.BoxSizer(wx.VERTICAL)
        self.label_dict = {}

        panel_upper = wx.Panel(self)
        box_upper = wx.BoxSizer(wx.HORIZONTAL)
        # i = 0
        # for column in data.columns:
        #     cb1 = wx.CheckBox(panel_upper, label=column)
        #     cb1.SetValue(True)
        #     box_upper.Add(cb1, 1, wx.EXPAND | wx.LEFT, 15)
        #     self.Bind(wx.EVT_CHECKBOX, self.on_checked)
        #     self.label_dict[column] = i
        #     i += 1
        # panel_upper.SetSizer(box_upper)
        # self.box_main.Add(panel_upper)

        panel_lower = wx.lib.scrolledpanel.ScrolledPanel(self, size=(1000,-1))
        panel_lower.SetupScrolling()
        panel_lower.SetBackgroundColour("White")
        self.box_lower = wx.BoxSizer(wx.HORIZONTAL)

        box_local = wx.BoxSizer(wx.VERTICAL)
        plt = Figure(figsize=(20,10))
        num_columns = len(df_arr)
        axes_1 = plt.add_subplot(1, num_columns, 1)
        # data_numpy = data[data.columns[0]].to_numpy()
        plt.gca().invert_yaxis()
        plt.subplots_adjust(left=0.01, right=1.00, top=0.95, bottom=0.05)
        depth = df_arr[0].index.to_numpy()
        axes_1.plot(df_arr[0][df_field].to_numpy(), depth)
        for i in range(1, num_columns):
            depth = df_arr[i].index.to_numpy()
            axes_tmp = plt.add_subplot(1, num_columns, i+1, sharey=axes_1)
            axes_tmp.set(xlabel=df_field, ylabel='Depth', title='Depth vs ' + df_field)

            data_numpy = df_arr[i][df_field].to_numpy()

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
        self.box_main.Add(box_nav, 0, wx.CENTER)
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

