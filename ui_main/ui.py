import wx
import wx.xrc
import wx.lib.agw.customtreectrl as CT


class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"First frame", pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        # MenuBar
        self.menubar = wx.MenuBar(0)

        self.file_menu = wx.Menu()
        self.exit_menu = wx.MenuItem(self.file_menu, wx.ID_EXIT, u"Exit")
        self.file_menu.Append(self.exit_menu)
        self.menubar.Append(self.file_menu, u"File")

        self.las_menu = wx.Menu()
        self.load_menu = wx.MenuItem(self.las_menu, wx.ID_ANY, u"Load LAS")
        self.las_menu.Append(self.load_menu)
        self.menubar.Append(self.las_menu, u"LAS")

        self.tools_menu = wx.Menu()
        self.plot_menu = wx.Menu()

        self.log_plot_menu = wx.MenuItem(self.plot_menu, wx.ID_ANY, u"Log Plot")
        self.plot_menu.Append(self.log_plot_menu)
        self.cross_plot_menu = wx.MenuItem(self.plot_menu, wx.ID_ANY, u"Cross Plot")
        self.plot_menu.Append(self.cross_plot_menu)
        self.tools_menu.AppendSubMenu(self.plot_menu, u"Plot")

        self.interpolation_menu = wx.Menu()
        self.validation_menu = wx.MenuItem(self.interpolation_menu, wx.ID_ANY, u"Validation")
        self.interpolation_menu.Append(self.validation_menu)
        self.prediction_menu = wx.MenuItem(self.interpolation_menu, wx.ID_ANY, u"Prediction")
        self.interpolation_menu.Append(self.prediction_menu)
        self.tools_menu.AppendSubMenu(self.interpolation_menu, u"Interpolate")
        self.menubar.Append(self.tools_menu, u"Tools")

        self.SetMenuBar(self.menubar)

        self.box_main = wx.BoxSizer(wx.HORIZONTAL)
        panel_left = wx.Panel(self)
        panel_left.SetBackgroundColour(wx.Colour(221, 221, 221))

        self.box_left = wx.BoxSizer(wx.VERTICAL)
        panel_left.SetSizer(self.box_left)
        self.staticText1 = wx.StaticText(self, label="Projects:")

        self.left_tree = CT.CustomTreeCtrl(self, agwStyle = CT.TR_AUTO_CHECK_CHILD | CT.TR_AUTO_CHECK_PARENT)
        self.box_left.Add(self.left_tree, 1, wx.EXPAND, border=5)
        self.root = self.left_tree.AddRoot("Wells")

        self.left_tree.ExpandAll()

        self.box_main.Add(panel_left, 1, wx.EXPAND)
        panel_right = wx.Panel(self)

        self.box_main.Add(panel_right, 4, wx.EXPAND)

        self.SetSizer(self.box_main)
        self.Centre(wx.BOTH)
        self.Maximize()

        # Connect Events
        self.Bind(wx.EVT_MENU, self.load_las, id=self.load_menu.GetId())
        self.Bind(wx.EVT_MENU, self.plot_log, id=self.log_plot_menu.GetId())
        self.Bind(wx.EVT_MENU, self.cross_plot, id=self.cross_plot_menu.GetId())
        self.Bind(wx.EVT_MENU, self.on_prediction, id=self.prediction_menu.GetId())
        self.Bind(wx.EVT_MENU, self.on_validation, id=self.validation_menu.GetId())

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def load_las(self, event):
        event.Skip()

    def plot_log(self, event):
        event.Skip()

    def cross_plot(self, event):
        event.Skip()

    def add_well(self, tree, name):
        return self.left_tree.AppendItem(self.root, name, ct_type=1)

    def add_las_to_well(self, tree, name):
        return self.left_tree.AppendItem(tree, name, ct_type=1)

    def on_prediction(self, event):
        event.Skip()

    def on_validation(self, event):
        event.Skip()