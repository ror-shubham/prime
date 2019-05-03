import os
import wx
from utils.chromium_panel import ChromiumPanel
from utils.map_string_to_color import get_colors_for_list_string
from plotly.offline import plot
import plotly.graph_objs as go
import numpy as np
from itertools import chain


def facies_csv_dlg(parent):
    wildcard = "Facies CSV (*.csv)|*.csv"
    home_dir = os.path.expanduser('~')
    prime_dir = os.path.join(home_dir, 'PrimeProjects')
    dlg = wx.FileDialog(
        parent,
        message="Select csv for facies",
        defaultFile="",
        wildcard=wildcard,
        style=wx.FD_OPEN,
        defaultDir=prime_dir if os.path.exists(home_dir) else home_dir
    )
    if dlg.ShowModal() == wx.ID_OK:
        path = dlg.GetPath()
        dlg.Destroy()
        return path
    dlg.Destroy()


def plot_3d_facies(plotter, data):
    data = data.sample(frac=0.01)
    color_list = data['facies'].unique()
    color_length = len(color_list)
    color_dict = get_colors_for_list_string(color_list)
    color_value_list = list(color_dict.values())
    col_nums = np.linspace(0, 1, color_length+1)
    # # TODO make the sample taking dynamic based on data size
    x = data.lat
    y = data.long
    z = -1 * data.DEPTH
    w = data['facies']
    colorscale1 = list(
        map(
            lambda i : ([col_nums[i], color_value_list[i]], [col_nums[i+1], color_value_list[i]]), range(color_length)
        ))
    colorscale = list(chain.from_iterable(colorscale1))
    print(colorscale)
    cmin = -0.5
    cmax = color_length - 0.5
    trace3d = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=7,
            line=dict(width=1),
            colorbar=dict(
                title='Month',
                tickvals = list(range(len(color_list))),
                ticktext = color_list
            ),
            colorscale = colorscale,
            cmin=cmin,
            cmax=cmax,
            color=list(map(lambda x: color_dict[x], w)),
        ),

        text=w,
        hoverinfo="x+y+z+text"
    )
    data = [trace3d]
    layout = go.Layout(
        title='facies' + " 3d plot",
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
    plotter.nb.AddPage(pnl, "3d plot-facies")
