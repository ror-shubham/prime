import wx
import wx.html2

from plotly import tools
import plotly.graph_objs as go
from plotly.offline import plot


class SelectCorrelationPlotField(wx.Dialog):
    def __init__(self, parent, choices):
        wx.Dialog.__init__(self, parent, title="Select Field to correlation plot")

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


class PlotCorrelation():
    def __init__(self, parent, plotter, df_arr, df_field):
        depths = list(map(lambda df: df.index.to_numpy(), df_arr))
        y_ndarr = list(map(lambda df: df[df_field].to_numpy(), df_arr))
        # todo add real title here
        plot_titles = list(map(lambda x: df_field + " vs Depth", df_arr))

        num_columns = len(depths)
        fig = tools.make_subplots(rows=1, cols=num_columns,
                                  shared_yaxes=True,
                                  shared_xaxes=True,
                                  vertical_spacing=0.001,
                                  subplot_titles=plot_titles,
                                  )

        for i in range(1, num_columns+1):
            trace = go.Scatter(
                x=y_ndarr[i-1],
                y=depths[i-1],
                name=plot_titles[i-1]
            )
            fig.append_trace(trace, 1, i)

        fig['layout'].update(
            legend=dict(x=-0.03,
                        y=1, ),
            hovermode='closest'
        )
        fig['layout'].update(width=600 * num_columns)
        for i in range(1, num_columns):
            fig['layout']['yaxis'].update(title='Depth', autorange='reversed')
            fig['layout']['xaxis' + str(i)].update(title=df_field, showspikes= True)

        html_string = plot(fig, output_type='div')

        browser = wx.html2.WebView.New(parent)
        browser.SetPage(html_string, "")

        plotter.nb.AddPage(browser, "Correlation plot " + df_field)
