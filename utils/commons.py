import wx
import wx.html2


def show_message_dialog(parent, message, title):
    dlg = wx.MessageDialog(parent,
                           message,
                           title,
                           wx.OK | wx.ICON_INFORMATION
                           )
    dlg.ShowModal()
    dlg.Destroy()

def add_html_to_browser_page(parent, plotter, html_string, title):
    browser = wx.html2.WebView.New(parent)
    browser.SetPage(html_string, "")
    plotter.nb.AddPage(browser, title)
    parent.Layout()