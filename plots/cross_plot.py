import os

from utils.commons import show_message_dialog

import wx

import plotly.graph_objs as go
from plotly.offline import plot


class SetCrossPlotProperties(wx.Dialog):
    def __init__(self, parent, choices):
        self.choices = choices
        wx.Dialog.__init__(self, parent, title="Select properties")

        self.box_main = wx.BoxSizer(wx.VERTICAL)

        self.static_well = wx.StaticText(self, wx.ID_ANY, u"Select properties for cross plot: ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_well.Wrap(-1)
        self.box_main.Add(self.static_well, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        self.box_checks = wx.BoxSizer(wx.HORIZONTAL)
        self.choice_box_1 = wx.Choice(self, choices=choices)
        self.choice_box_1.SetSelection(0)
        self.box_checks.Add(self.choice_box_1, 1)
        self.choice_box_2 = wx.Choice(self, choices=choices)
        self.choice_box_2.SetSelection(1)
        self.box_checks.Add(self.choice_box_2, 1)
        self.box_main.Add(self.box_checks, 1, wx.EXPAND, 5)

        box_buttons = wx.StdDialogButtonSizer()
        self.btn_ok = wx.Button(self, wx.ID_OK)
        self.btn_ok.Bind(wx.EVT_BUTTON, self.on_ok_click)
        box_buttons.AddButton(self.btn_ok)
        self.btn_cancel = wx.Button(self, wx.ID_CANCEL)
        box_buttons.AddButton(self.btn_cancel)
        box_buttons.Realize()

        self.box_main.Add(box_buttons, 1, wx.EXPAND, 5)

        self.SetSizer(self.box_main)
        self.Layout()
        self.box_main.Fit(self)

        self.Centre(wx.BOTH)

    def get_selection(self):
        return self.choice_box_1.GetStringSelection(), self.choice_box_2.GetStringSelection()

    def on_ok_click(self, e):
        selected = self.get_selection()
        if selected[0] == selected[1]:
            show_message_dialog(self, "Both the properties should not be same", "Error")
        else:
            self.EndModal(wx.ID_OK)


class PlotCross(object):
    def __init__(self, data, props_to_relate):
        plot_title = props_to_relate[0] + ' vs' + props_to_relate[1]
        x = data[props_to_relate[1]].to_numpy()
        y = data[props_to_relate[0]].to_numpy()

        trace1 = go.Scatter(
            x=x,
            y=y,
            mode = 'markers'
        )
        layout = go.Layout(
            title=plot_title,
            xaxis=dict(
                title=props_to_relate[1],
                showspikes=True
            ),
            yaxis=dict(
                title=props_to_relate[0],
                showspikes=True
            ),
            autosize=True,
            margin=dict(
                l=65,
                r=50,
                b=65,
                t=150
            ),
        )
        fig = go.Figure(data=[trace1], layout=layout)
        fig['layout'].update(
            legend=dict(x=-0.03,
                        y=1, ),
            hovermode='closest'
        )
        home_dir = os.path.expanduser('~')
        prime_dir = os.path.join(home_dir, 'PrimeProjects')
        html_dir = prime_dir if os.path.exists(prime_dir) else home_dir
        self.html_file_path = plot(fig, filename=os.path.join(html_dir, 'temp.html'), auto_open=False)

    def get_html_file_path(self):
        return self.html_file_path
