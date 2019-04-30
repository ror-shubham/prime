# source of formulae https://www.cgg.com/data/1/rec_docs/883_shale_volume_calculation.pdf

from plotly import tools
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.figure_factory as ff

import numpy as np
import wx
import wx.html2



class GrAnalysis(object):
    def __init__(self, data, gr_min_max):
        plot_title = "Vshale plots"
        depth_nd_arr = data.index.to_numpy()
        try:
            gr_nd_arr = data.gr.to_numpy()
        except AttributeError:
            gr_nd_arr = data.GR.to_numpy()

        plot_titles = ['GR plot',
                       'Linear Vshale',
                       'Larionov Tertiary rocks',
                       'Steiber',
                       'Clavier',
                       'Larionov older rock'
                       ]
        fig = tools.make_subplots(rows=1, cols=6,
                                  shared_yaxes=True,
                                  vertical_spacing=0.001,
                                  subplot_titles=plot_titles,
                                  )

        gr_min = gr_min_max[0]
        gr_max = gr_min_max[1]
        igr = (gr_nd_arr - gr_min) / (gr_max - gr_min)
        trace1 = go.Scatter(
            x=gr_nd_arr,
            y=depth_nd_arr,
        )
        fig.append_trace(trace1, 1, 1)
        trace2 = go.Scatter(
            x=igr,
            y=depth_nd_arr,
        )
        fig.append_trace(trace2, 1, 2)
        larionov_gr = 0.083 * (2 ** (3.7 * igr) - 1)
        trace3 = go.Scatter(
            x=larionov_gr,
            y=depth_nd_arr,
        )
        fig.append_trace(trace3, 1, 3)
        steiber_gr = igr / (3 - 2 * igr)
        trace4 = go.Scatter(
            x=steiber_gr,
            y=depth_nd_arr,
        )
        fig.append_trace(trace4, 1, 4)
        clavier_gr = 1.7 - (((3.38) - ((igr + 0.7) ** 2)) ** 0.5)
        trace5 = go.Scatter(
            x=clavier_gr,
            y=depth_nd_arr,
        )
        fig.append_trace(trace5, 1, 5)
        larionov_older_gr = 0.33 * ((2 ** (2 * igr)) - 1)
        trace6 = go.Scatter(
            x=larionov_older_gr,
            y=depth_nd_arr,
        )
        fig.append_trace(trace6, 1, 6)

        fig['layout'].update(
            legend=dict(x=-0.03,
                        y=1, ),
            hovermode='closest'
        )
        self.html_string = plot(fig, output_type='div')

    def get_html_string(self):
        return self.html_string


class GrMinMaxSelect(wx.Dialog):

    def __init__(self, parent, data):
        try:
            gr_nd_arr = data.gr.to_numpy()
        except AttributeError:
            gr_nd_arr = data.GR.to_numpy()
        gr_min = np.nanmin(gr_nd_arr)
        gr_max = np.nanmax(gr_nd_arr)
        wx.Dialog.__init__(self, None, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER, size=(700, 700))

        hbox = wx.BoxSizer(wx.VERTICAL)

        htmlSizer = wx.BoxSizer(wx.VERTICAL)
        htmlPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition)
        browser = wx.html2.WebView.New(htmlPanel)
        html_string = get_html_distribution(gr_nd_arr)
        browser.SetPage(html_string, "")
        htmlSizer.Add(browser, 1, wx.EXPAND)
        htmlPanel.SetSizer(htmlSizer)
        htmlSizer.Fit(htmlPanel)

        hbox.Add(htmlPanel, 1, wx.EXPAND | wx.ALL, 5)

        sizer_local4 = wx.BoxSizer(wx.VERTICAL)
        sizer_text_ctr = wx.BoxSizer(wx.HORIZONTAL)
        sizer_local_1 = wx.BoxSizer(wx.VERTICAL)
        self.static_local_1 = wx.StaticText(self, wx.ID_ANY, u"Select GRmin", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_local_1.Add(self.static_local_1, 0, wx.ALL, 5)
        self.text_ctrl_min = wx.TextCtrl(self, wx.ID_ANY, str(gr_min), wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_local_1.Add(self.text_ctrl_min, 0, wx.ALL, 5)
        sizer_text_ctr.Add(sizer_local_1, 1, wx.EXPAND, 5)
        sizer_local_max = wx.BoxSizer(wx.VERTICAL)
        self.static_local_2 = wx.StaticText(self, wx.ID_ANY, u"Select GRmax", wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_local_max.Add(self.static_local_2, 0, wx.ALL, 5)
        self.text_ctrl_max = wx.TextCtrl(self, wx.ID_ANY, str(gr_max), wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_local_max.Add(self.text_ctrl_max, 0, wx.ALL, 5)
        sizer_text_ctr.Add(sizer_local_max, 1, wx.EXPAND, 5)
        sizer_local4.Add(sizer_text_ctr, 1, wx.EXPAND, 5)
        sizer_btn = wx.StdDialogButtonSizer()
        self.sizer_btnOK = wx.Button(self, wx.ID_OK)
        sizer_btn.AddButton(self.sizer_btnOK)
        self.sizer_btnCancel = wx.Button(self, wx.ID_CANCEL)
        sizer_btn.AddButton(self.sizer_btnCancel)
        sizer_btn.Realize()
        sizer_local4.Add(sizer_btn, 1, wx.EXPAND, 5)
        hbox.Add(sizer_local4, 0, wx.EXPAND, 5)
        self.SetSizer(hbox)
        self.Maximize()
        self.Layout()
        hbox.Fit(self)
        self.Centre(wx.BOTH)

    def get_min_max(self):
        gr_min = float(self.text_ctrl_min.GetValue())
        gr_max = float(self.text_ctrl_max.GetValue())
        return gr_min, gr_max


def get_html_distribution(gr_nd_arr):
    y = gr_nd_arr[~np.isnan(gr_nd_arr)]

    hist_data = [y]
    group_labels = ['GR dist plot']

    fig = ff.create_distplot(hist_data, group_labels)
    return plot(fig, output_type='div')
