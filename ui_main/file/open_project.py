import os
import wx


def open_project_dlg(parent):
    wildcard = "Project source (*.prime)|*.prime"
    home_dir = os.path.expanduser('~')
    prime_dir = os.path.join(home_dir, 'PrimeProjects')
    dlg = wx.FileDialog(
        parent,
        message="Open a prime project",
        defaultFile="",
        wildcard=wildcard,
        style=wx.FD_OPEN,
        defaultDir=prime_dir if os.path.exists(home_dir) else home_dir
    )
    if dlg.ShowModal() == wx.ID_OK:
        path = dlg.GetPath()
        dlg.Destroy()
        return path
    dlg.Destroy()