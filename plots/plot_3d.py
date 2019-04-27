import os
import pwd

from utils.chromium_panel import MainPanel
from plotly.offline import plot
import plotly.graph_objs as go


def plot_3d(plotter, data):
    data = data.sample(frac=0.01)
    # # TODO make the sample taking dynamic based on data size
    x = data.lat
    y = data.long
    z = -1 * data.DEPTH
    prop_ind = data.columns[3]
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
        hoverinfo = "x+y+z+text"
    )
    data = [trace3d]
    layout = go.Layout(
        title=prop_ind+" 3d plot",
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
    home_dir = pwd.getpwuid(os.getuid()).pw_dir
    prime_dir = pwd.getpwuid(os.getuid()).pw_dir + '/PrimeProjects'
    html_dir = prime_dir if os.path.exists(prime_dir) else home_dir
    html_file_path = plot(fig, filename=html_dir+'/temp.html', auto_open=False)

    pnl = MainPanel(plotter.nb, html_file_path)
    plotter.nb.AddPage(pnl, "3d plot")


