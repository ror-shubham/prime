import wx

from utils.chromium_panel import ChromiumPanel


def show_message_dialog(parent, message, title):
    dlg = wx.MessageDialog(parent,
                           message,
                           title,
                           wx.OK | wx.ICON_INFORMATION
                           )
    dlg.ShowModal()
    dlg.Destroy()


def add_html_to_browser_page(parent, plotter, html_file_path, title):
    pnl = ChromiumPanel(plotter.nb, html_file_path)
    plotter.nb.AddPage(pnl, title, select=True)
    parent.Layout()
