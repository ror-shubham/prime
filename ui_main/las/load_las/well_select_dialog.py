import wx
import wx.xrc


class SelectWellDialog(wx.Dialog):

    def __init__(self, parent, choices, default_name):
        wx.Dialog.__init__(self, parent, title="Select Well ID")

        box_main = wx.BoxSizer(wx.VERTICAL)
        box_well_id = wx.BoxSizer(wx.VERTICAL)

        self.static_well = wx.StaticText(self, wx.ID_ANY, u"Well ID: ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_well.Wrap(-1)

        box_well_id.Add(self.static_well, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.combo_box = wx.ComboBox(self, value=default_name, choices=choices)
        box_well_id.Add(self.combo_box, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

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

    def get_well_name(self):
        return self.combo_box.GetValue()
