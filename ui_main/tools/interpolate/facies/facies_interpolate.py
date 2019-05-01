import os
import wx


def facies_csv_dlg(parent):
    wildcard = "Facies CSV (*.csv)|*.csv"
    home_dir = os.path.expanduser('~')
    prime_dir = os.path.join(home_dir, 'PrimeProjects')
    dlg = wx.FileDialog(
        parent,
        message="Select csv for facies",
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