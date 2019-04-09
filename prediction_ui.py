import wx
import wx.xrc


class PredictionDialog(wx.Dialog):

    def __init__(self, parent, common_fields):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                           style=wx.DEFAULT_DIALOG_STYLE)

        sizer_main = wx.BoxSizer(wx.VERTICAL)

        sizer_num_wells = wx.BoxSizer(wx.HORIZONTAL)

        self.static_num_wells = wx.StaticText(self, wx.ID_ANY, u"Number of wells to be interpolated", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.static_num_wells.Wrap(-1)

        sizer_num_wells.Add(self.static_num_wells, 0, wx.ALL, 5)

        self.text_ctrl_num_wells = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        sizer_num_wells.Add(self.text_ctrl_num_wells, 0, wx.ALL, 5)

        sizer_main.Add(sizer_num_wells, 1, wx.EXPAND, 5)

        sizer_props = wx.BoxSizer(wx.HORIZONTAL)

        self.static_props = wx.StaticText(self, wx.ID_ANY, u"Property to be interpolated", wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        self.static_props.Wrap(-1)

        sizer_props.Add(self.static_props, 0, wx.ALL, 5)

        self.choice_props = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, common_fields, 0)
        self.choice_props.SetSelection(0)
        sizer_props.Add(self.choice_props, 0, wx.ALL, 5)

        sizer_main.Add(sizer_props, 1, wx.EXPAND, 5)

        sizer_method = wx.BoxSizer(wx.HORIZONTAL)

        self.static_methods = wx.StaticText(self, wx.ID_ANY, u"Interpolation method: ", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.static_methods.Wrap(-1)
        methods_choices = ["linear", "svm"]
        self.choice = wx.Choice(self, choices=methods_choices)
        self.choice.SetSelection(0)

        sizer_method.Add(self.static_methods, 0, wx.ALL, 5)
        sizer_method.Add(self.choice, 1, wx.ALL, 5)

        sizer_main.Add(sizer_method, 1, wx.EXPAND, 5)

        dialog_btn_sizer = wx.StdDialogButtonSizer()
        self.btn_ok = wx.Button(self, wx.ID_OK)
        dialog_btn_sizer.AddButton(self.btn_ok)
        self.btn_cancel = wx.Button(self, wx.ID_CANCEL)
        dialog_btn_sizer.AddButton(self.btn_cancel)
        dialog_btn_sizer.Realize()

        sizer_main.Add(dialog_btn_sizer, 1, wx.EXPAND, 5)

        self.SetSizer(sizer_main)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass
