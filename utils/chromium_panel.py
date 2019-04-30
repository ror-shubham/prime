import wx
import wx.lib.inspection
from cefpython3 import cefpython as cef
import platform
import sys

WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# TODO bring back onresize

if MAC:
    try:
        from AppKit import NSApp
    except ImportError:
        print("[wxpython.py] Error: PyObjC package is missing, "
              "cannot fix Issue #371")
        print("[wxpython.py] To install PyObjC type: "
              "pip install -U pyobjc")
        sys.exit(1)


class ChromiumPanel(wx.Panel):
    def __init__(self, parent, html_file_path):
        self.html_file_path = html_file_path
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY,
                          )

        self.browser = None
        settings = {}
        if MAC:
            settings["external_message_pump"] = True
        cef.Initialize(settings=settings)

        if MAC:
            NSApp.windows()[0].contentView().setWantsLayer_(True)

        if LINUX:
            wx.CallLater(100, self.embed_browser)
        else:
            self.embed_browser()

    def embed_browser(self):
        window_info = cef.WindowInfo()
        (width, height) = self.GetClientSize().Get()
        window_info.SetAsChild(self.GetHandle(),
                               [0, 0, width, height])
        self.browser = cef.CreateBrowserSync(window_info,
                                             url="file://"+self.html_file_path)
        self.browser.SetClientHandler(FocusHandler())


class FocusHandler(object):
    def OnGotFocus(self, browser, **_):
        # Temporary fix for focus issues on Linux (Issue #284).
        if LINUX:
            print("[wxpython.py] FocusHandler.OnGotFocus:"
                  " keyboard focus fix (Issue #284)")
            browser.SetFocus(True)
