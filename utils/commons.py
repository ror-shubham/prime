import wx


def show_message_dialog(parent, message, title):
    dlg = wx.MessageDialog(parent,
                           message,
                           title,
                           wx.OK | wx.ICON_INFORMATION
                           )
    dlg.ShowModal()
    dlg.Destroy()