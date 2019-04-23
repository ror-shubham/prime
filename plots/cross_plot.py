import wx
import wx.xrc
import wx.lib.scrolledpanel

import matplotlib

from plots.generic_plot import PlotCanvas

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
        depths = list(map(lambda df: df.index.to_numpy(), df_arr))
        y_ndarr = list(map(lambda df: df[df_field].to_numpy(), df_arr))
        plot_titles = list(map(lambda x: "a", df_arr))
        xlabel = df_field
        ylabel = 'Depth'
        self.frame = PlotCanvas(None, -1, "Cross Plot", plot_titles, depths, y_ndarr, xlabel, ylabel)
        self.frame.Show(True)
        self.app.MainLoop()
