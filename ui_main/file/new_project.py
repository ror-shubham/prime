import pwd

import wx
import wx.lib.filebrowsebutton as filebrowse
import os
import pathlib


# TODO form validation for filename
class NewProjectDialog(wx.Dialog):
    def __init__(self, parent):
        self.project_path = ''
        self.home_dir = pwd.getpwuid(os.getuid()).pw_dir + '/PrimeProjects'
        pathlib.Path(self.home_dir).mkdir(parents=True, exist_ok=True)

        wx.Dialog.__init__(self, parent, title="Set Project Name")

        box_main = wx.BoxSizer(wx.VERTICAL)
        box_name = wx.BoxSizer(wx.HORIZONTAL)

        self.static_name = wx.StaticText(self, wx.ID_ANY, u"Project Name: ", size = wx.DefaultSize)
        box_name.Add(self.static_name, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        self.project_text = wx.TextCtrl(self)
        box_name.Add(self.project_text, 1, wx.ALIGN_LEFT | wx.ALL, 5)

        self.dbb = filebrowse.DirBrowseButton(
            self,
            -1,
            size=(450, -1),
            changeCallback=self.dbbCallback,
            labelText="Project Home",
            startDirectory = self.home_dir,
            name='dirBrowseButton'
        )
        self.dbb.textControl.SetValue(self.home_dir)
        box_main.Add(box_name, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        box_main.Add(self.dbb, 0, wx.ALIGN_CENTER | wx.ALL, 5)

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

        self.btn_ok.Bind(wx.EVT_BUTTON, self.on_submit)

    def dbbCallback(self, evt):
        self.home_dir = evt.GetString()

    def on_submit(self, event):
        project_path = os.path.join(self.home_dir, self.project_text.GetValue() + '.prime')
        project_exists = os.path.isfile(project_path)
        if project_exists:
            dlg = wx.MessageDialog(self,
                                   'The project already exists at the given path. Please rename or open the existing '
                                   'project',
                                   'Error',
                                   wx.OK | wx.ICON_INFORMATION
                                   )
            dlg.ShowModal()
            dlg.Destroy()
        else:
            pathlib.Path(project_path).touch()
            self.project_path = project_path
            self.EndModal(wx.ID_OK)

    def get_project_path(self):
        return self.project_path
