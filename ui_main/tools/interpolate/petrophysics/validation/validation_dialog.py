import wx
import wx.xrc


class ValidationDialog(wx.Dialog):

    def __init__(self, parent, common_fields):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                           size=wx.Size(942, 264),
                           style=wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_prop = wx.BoxSizer(wx.HORIZONTAL)

        self.static_prop = wx.StaticText(self, wx.ID_ANY, u"Property to be interpolated", wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        self.static_prop.Wrap(-1)

        sizer_prop.Add(self.static_prop, 0, wx.ALL, 5)

        self.choice_prop = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, common_fields, 0)
        self.choice_prop.SetSelection(0)
        sizer_prop.Add(self.choice_prop, 0, wx.ALL, 5)

        sizer_main.Add(sizer_prop, 1, wx.EXPAND, 5)

        sizer_interpolation = wx.BoxSizer(wx.HORIZONTAL)

        self.static_interpolation = wx.StaticText(self, wx.ID_ANY, u"Interpolation method: ", wx.DefaultPosition,
                                                  wx.DefaultSize, 0)
        self.static_interpolation.Wrap(-1)

        sizer_interpolation.Add(self.static_interpolation, 0, wx.ALL, 5)

        regression_choices = [u"linear", u"svm"]
        self.choice_method = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, regression_choices, 0)
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

    def get_selected_property(self):
        return self.choice_prop.GetStringSelection()

    def get_selected_method(self):
        return self.choice_method.GetStringSelection()

    def get_selected_scoring(self):
        return self.choice_scoring.GetStringSelection()
