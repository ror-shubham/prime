import os

from plotly import tools
import plotly.graph_objs as go
from plotly.offline import plot


class PlotLog(object):
    def __init__(self, data):
        plot_titles = list(map(lambda x: "Depth vs " + x, data.columns))
        x_ndarr = data.index.to_numpy()
        y_ndarr = list(map(lambda x: data[x].to_numpy(), data.columns))

        num_columns = len(y_ndarr)
        fig = tools.make_subplots(rows=1, cols=num_columns,
                                  shared_yaxes=True,
                                  vertical_spacing=0.001,
                                  subplot_titles=plot_titles,
                                  )

        for i in range(1, num_columns):
            trace = go.Scatter(
                x=y_ndarr[i-1],
                y=x_ndarr,
                name=plot_titles[i-1]
            )
            fig.append_trace(trace, 1, i)

        fig['layout'].update(
            legend=dict(x=-0.03,
                        y=1, ),
            hovermode='closest'
        )
        fig['layout'].update(width=600 * num_columns)
        fig['layout']['yaxis'].update(title='Depth', autorange='reversed')
        for i in range(1, num_columns):
            fig['layout']['xaxis' + str(i)].update(title=data.columns[i], showspikes= True)
        home_dir = os.path.expanduser('~')
        prime_dir = os.path.join(home_dir, 'PrimeProjects')
        html_dir = prime_dir if os.path.exists(prime_dir) else home_dir
        self.html_file_path = plot(fig, filename=os.path.join(html_dir, 'temp.html'), auto_open=False)

    def get_html_file_path(self):
        return self.html_file_path
