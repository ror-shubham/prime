import wx
from ui_main.file.open_project import open_project_dlg
from ui_main.file.new_project import NewProjectDialog
# TODO don't open anything if initia_dialog doesn't return


class InitialDialog(wx.Dialog):
    def __init__(self, parent):
        self.project_path = ''
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Set Project Name", pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.new_project_btn = wx.Button(self, wx.ID_ANY, u"Create New Project", wx.DefaultPosition, wx.DefaultSize, 0)
        main_sizer.Add(self.new_project_btn, 0, wx.ALL, 5)

        self.open_project_btn = wx.Button(self, wx.ID_ANY, u"Open existing project", wx.DefaultPosition, wx.DefaultSize,
                                          0)
        main_sizer.Add(self.open_project_btn, 0, wx.ALL, 5)

        self.SetSizer(main_sizer)
        self.Layout()
        main_sizer.Fit(self)

        self.Centre(wx.BOTH)

        self.new_project_btn.Bind(wx.EVT_BUTTON, self.on_new_click)
        self.open_project_btn.Bind(wx.EVT_BUTTON, self.on_open_click)

    def on_new_click(self, event):
        dlg = NewProjectDialog(self)
        dlg.SetSize(450, 80)
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val != wx.ID_OK:
            return
        else:
            self.project_path = dlg.get_project_path()
            self.EndModal(wx.ID_OK)
            # TODO file name validator here

    def on_open_click(self, event):
        self.project_path = open_project_dlg(self)
        if(self.project_path is not None):
            self.EndModal(wx.ID_OK)

    def get_project_path(self):
        return self.project_path
