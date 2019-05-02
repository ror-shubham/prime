import wx
import wx.xrc


class PredictionDialog(wx.Dialog):

    def __init__(self, parent, common_fields, methods_choices):
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

        sizer_method = wx.BoxSizer(wx.HORIZONTAL)

        self.static_methods = wx.StaticText(self, wx.ID_ANY, u"Interpolation method: ", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.static_methods.Wrap(-1)
        self.choice_method = wx.Choice(self, choices=methods_choices)
        self.choice_method.SetSelection(0)

        sizer_method.Add(self.static_methods, 0, wx.ALL, 5)
        sizer_method.Add(self.choice_method, 1, wx.ALL, 5)

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

    def get_num_wells(self):
        return self.text_ctrl_num_wells.GetValue()

    def get_selected_method(self):
        return self.choice_method.GetStringSelection()
