import os
import wx

from utils.chromium_panel import ChromiumPanel
from plotly.offline import plot
import plotly.graph_objs as go


class Plot3dDlg(wx.Dialog):

    def __init__(self, parent, choices, ):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_prop = wx.BoxSizer(wx.HORIZONTAL)

        self.static_prop = wx.StaticText(self, wx.ID_ANY, u"Select property to plot", wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        self.static_prop.Wrap(-1)

        sizer_prop.Add(self.static_prop, 4, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.choice_prop = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choices, 0)
        self.choice_prop.SetSelection(0)
        sizer_prop.Add(self.choice_prop, 2, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        sizer_main.Add(sizer_prop, 1, wx.EXPAND, 5)

        m_sdbSizer1 = wx.StdDialogButtonSizer()
        self.m_sdbSizer1OK = wx.Button(self, wx.ID_OK)
        m_sdbSizer1.AddButton(self.m_sdbSizer1OK)
        self.m_sdbSizer1Cancel = wx.Button(self, wx.ID_CANCEL)
        m_sdbSizer1.AddButton(self.m_sdbSizer1Cancel)
        m_sdbSizer1.Realize()

        sizer_main.Add(m_sdbSizer1, 1, wx.EXPAND, 5)

        self.SetSizer(sizer_main)
        self.Layout()
        sizer_main.Fit(self)

        self.Centre(wx.BOTH)

    def get_selection(self):
        return self.choice_prop.GetStringSelection()


def plot_3d(plotter, data, prop_to_plot, title):
    data = data.sample(frac=0.01)
    # # TODO make the sample taking dynamic based on data size
    x = data.lat
    y = data.long
    z = -1 * data.DEPTH
    prop_ind = prop_to_plot
    w = data[prop_ind]
    trace3d = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            color=w,
            colorscale='Viridis',
            colorbar=dict(
                thickness=20,
                title=prop_ind,
            ),
            opacity=0.9
        ),
        text=w,
        hoverinfo="x+y+z+text"
    )
    data = [trace3d]
    layout = go.Layout(
        title=prop_ind + " 3d plot",
        scene=dict(
            xaxis=dict(
                title='Latitude'),
            yaxis=dict(
                title='Longitude'),
            zaxis=dict(
                title='Depth'), ),
        autosize=True,
        margin=dict(
            l=65,
            r=50,
            b=65,
            t=90
        )
    )
    fig = go.Figure(data=data, layout=layout)
    home_dir = os.path.expanduser('~')
    prime_dir = os.path.join(home_dir, 'PrimeProjects')
    html_dir = prime_dir if os.path.exists(prime_dir) else home_dir
    html_file_path = plot(fig, filename=os.path.join(html_dir, 'temp.html'), auto_open=False)

    pnl = ChromiumPanel(plotter.nb, html_file_path)
    plotter.nb.AddPage(pnl, title)
