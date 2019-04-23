import os
import pwd
import wx


def open_project_dlg(parent):
    wildcard = "Project source (*.prime)|*.prime"
    home_dir = pwd.getpwuid(os.getuid()).pw_dir + '/PrimeProjects'
    dlg = wx.FileDialog(
        parent,
        message="Create new prime project",
        defaultFile="",
        wildcard=wildcard,
        style=wx.FD_OPEN,
        defaultDir=home_dir if os.path.exists(home_dir) else None
    )
    if dlg.ShowModal() == wx.ID_OK:
        path = dlg.GetPath()
        dlg.Destroy()
        return path
    dlg.Destroy()