import os

import wx
import wx.xrc

from plotly.offline import plot
import plotly.graph_objs as go


class ValidationDialog(wx.Dialog):

    def __init__(self, parent, common_fields, method_choices):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                           size=wx.Size(942, 264),
                           style=wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_interpolation = wx.BoxSizer(wx.HORIZONTAL)

        self.static_interpolation = wx.StaticText(self, wx.ID_ANY, u"Interpolation method: ", wx.DefaultPosition,
                                                  wx.DefaultSize, 0)
        self.static_interpolation.Wrap(-1)

        sizer_interpolation.Add(self.static_interpolation, 0, wx.ALL, 5)

        self.choice_method = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, method_choices, 0)
        self.choice_method.SetSelection(0)
        sizer_interpolation.Add(self.choice_method, 0, wx.ALL, 5)

        sizer_main.Add(sizer_interpolation, 1, wx.EXPAND, 5)

        sizer_scoring = wx.BoxSizer(wx.HORIZONTAL)

        self.static_scoring = wx.StaticText(self, wx.ID_ANY, u"Scoring", wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_scoring.Wrap(-1)

        sizer_scoring.Add(self.static_scoring, 0, wx.ALL, 5)

        scoring_choices = ['accuracy', 'adjusted_mutual_info_score', 'adjusted_rand_score', 'average_precision', 'balanced_accuracy', 'brier_score_loss', 'completeness_score', 'explained_variance', 'f1', 'f1_macro', 'f1_micro', 'f1_samples', 'f1_weighted', 'fowlkes_mallows_score', 'homogeneity_score', 'mutual_info_score', 'neg_log_loss', 'neg_mean_absolute_error', 'neg_mean_squared_error', 'neg_mean_squared_log_error', 'neg_median_absolute_error', 'normalized_mutual_info_score', 'precision', 'precision_macro', 'precision_micro', 'precision_samples', 'precision_weighted', 'r2', 'recall', 'recall_macro', 'recall_micro', 'recall_samples', 'recall_weighted', 'roc_auc', 'v_measure_score']
        self.choice_scoring = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, scoring_choices, 0)
        self.choice_scoring.SetSelection(27)
        sizer_scoring.Add(self.choice_scoring, 0, wx.ALL, 5)

        sizer_main.Add(sizer_scoring, 1, wx.EXPAND, 5)

        dlg_btn_sizer = wx.StdDialogButtonSizer()
        self.btn_ok = wx.Button(self, wx.ID_OK)
        dlg_btn_sizer.AddButton(self.btn_ok)
        self.btn_cancel = wx.Button(self, wx.ID_CANCEL)
        dlg_btn_sizer.AddButton(self.btn_cancel)
        dlg_btn_sizer.Realize()

        sizer_main.Add(dlg_btn_sizer, 1, wx.EXPAND, 5)

        self.SetSizer(sizer_main)
        self.Layout()

        self.Centre(wx.BOTH)

    def get_selected_method(self):
        return self.choice_method.GetStringSelection()

    def get_selected_scoring(self):
        return self.choice_scoring.GetStringSelection()


class ValidationPlot:
    def __init__(self, scores_df, title):
        data = []

        for column in scores_df:
            trace = go.Box(
                y=scores_df[column],
                name=column
            )
            data.append(trace)

        layout = go.Layout(
            title=go.layout.Title(
                text=title
            ),
            xaxis=go.layout.XAxis(
                title=go.layout.xaxis.Title(
                    text='Properties'
                )
            ),
            yaxis=go.layout.YAxis(
                title=go.layout.yaxis.Title(
                    text='Validation Scoring'
                )
            )
        )

        fig = go.Figure(data=data, layout=layout)

        home_dir = os.path.expanduser('~')
        prime_dir = os.path.join(home_dir, 'PrimeProjects')
        html_dir = prime_dir if os.path.exists(prime_dir) else home_dir
        self.html_file_path = plot(fig, filename=os.path.join(html_dir, 'temp.html'), auto_open=False)

    def get_html_file_path(self):
        return self.html_file_path
