import os

import wx
import wx.xrc
import wx.lib.agw.customtreectrl as CT


class MainFrame(wx.Frame):
    def __init__(self, parent, project_path):
        project_name = os.path.basename(project_path)[:-6]  # [:-6] remove '.prime' from name
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"First frame", pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        # MenuBar
        self.menubar = wx.MenuBar(0)

        self.file_menu = wx.Menu()
        self.new_project_menu = wx.MenuItem(self.file_menu, wx.ID_NEW, u"New Project")
        self.file_menu.Append(self.new_project_menu)
        self.save_project_menu = wx.MenuItem(self.file_menu, wx.ID_SAVE, u"Save Project")
        self.file_menu.Append(self.save_project_menu)
        self.open_project_menu = wx.MenuItem(self.file_menu, wx.ID_OPEN, u"Open Project")
        self.file_menu.Append(self.open_project_menu)
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
        self.correlation_plot_menu = wx.MenuItem(self.plot_menu, wx.ID_ANY, u"Correlation Plot")
        self.plot_menu.Append(self.correlation_plot_menu)
        self.overlay_plot_menu = wx.MenuItem(self.plot_menu, wx.ID_ANY, u"Overlay Plot")
        self.plot_menu.Append(self.overlay_plot_menu)
        self.cross_plot_menu = wx.MenuItem(self.plot_menu, wx.ID_ANY, u"Cross Plot")
        self.plot_menu.Append(self.cross_plot_menu)
        self.tools_menu.AppendSubMenu(self.plot_menu, u"Plot")

        self.interpolation_menu = wx.Menu()
        self.petrophysics_menu = wx.Menu()
        self.interpolation_menu.AppendSubMenu(self.petrophysics_menu, u"Petrophysics")
        self.validation_menu = wx.MenuItem(self.petrophysics_menu, wx.ID_ANY, u"Validation")
        self.petrophysics_menu.Append(self.validation_menu)
        self.prediction_menu = wx.MenuItem(self.petrophysics_menu, wx.ID_ANY, u"Prediction")
        self.petrophysics_menu.Append(self.prediction_menu)
        self.plot_3d_menu = wx.MenuItem(self.petrophysics_menu, wx.ID_ANY, u"3d Plot")
        self.petrophysics_menu.Append(self.plot_3d_menu)
        self.tools_menu.AppendSubMenu(self.interpolation_menu, u"Interpolate")

        self.facies_menu = wx.Menu()
        self.interpolation_menu.AppendSubMenu(self.facies_menu, u"Facies")
        self.interpolate_facies = wx.MenuItem(self.facies_menu, wx.ID_ANY, u"Interpolate")
        self.facies_menu.Append(self.interpolate_facies)

        self.menubar.Append(self.tools_menu, u"Tools")

        self.analysis_menu = wx.Menu()
        self.vshale_menu = wx.Menu()
        self.gr_vshale_menu = wx.MenuItem(self.vshale_menu, wx.ID_ANY, u"GR")
        self.vshale_menu.Append(self.gr_vshale_menu)
        self.analysis_menu.AppendSubMenu(self.vshale_menu, u"Vshale")
        self.menubar.Append(self.analysis_menu, u"Analysis")

        self.SetMenuBar(self.menubar)

        self.box_main = wx.BoxSizer(wx.HORIZONTAL)
        panel_left = wx.Panel(self)
        panel_left.SetBackgroundColour(wx.Colour(221, 221, 221))

        self.box_left = wx.BoxSizer(wx.VERTICAL)
        panel_left.SetSizer(self.box_left)
        self.staticText1 = wx.StaticText(panel_left, label="Projects:")
        self.box_left.Add(self.staticText1, 0)

        self.left_tree = CT.CustomTreeCtrl(panel_left, agwStyle = CT.TR_AUTO_CHECK_CHILD | CT.TR_AUTO_CHECK_PARENT)
        self.box_left.Add(self.left_tree, 1, wx.EXPAND, border=5)
        self.root = self.left_tree.AddRoot(project_name)

        self.left_tree.ExpandAll()

        self.box_main.Add(panel_left, 1, wx.EXPAND)

        self.box_right = wx.BoxSizer(wx.VERTICAL)
        self.panel_right = wx.Panel(self)
        self.panel_right.SetBackgroundColour(wx.Colour(0,0,0))
        self.panel_right.SetSizer(self.box_right)
        self.box_main.Add(self.panel_right, 6, wx.EXPAND)

        self.SetSizer(self.box_main)
        self.Centre(wx.BOTH)
        self.Maximize()

        # Connect Events
        self.Bind(wx.EVT_MENU, self.new_project, id=self.new_project_menu.GetId())
        self.Bind(wx.EVT_MENU, self.save_project, id=self.save_project_menu.GetId())
        self.Bind(wx.EVT_MENU, self.open_project, id=self.open_project_menu.GetId())

        self.Bind(wx.EVT_MENU, self.load_las_dlg, id=self.load_menu.GetId())

        self.Bind(wx.EVT_MENU, self.plot_log, id=self.log_plot_menu.GetId())
        self.Bind(wx.EVT_MENU, self.correlation_plot, id=self.correlation_plot_menu.GetId())
        self.Bind(wx.EVT_MENU, self.overlay_plot, id=self.overlay_plot_menu.GetId())
        self.Bind(wx.EVT_MENU, self.cross_plot, id=self.cross_plot_menu.GetId())

        self.Bind(wx.EVT_MENU, self.on_prediction, id=self.prediction_menu.GetId())
        self.Bind(wx.EVT_MENU, self.on_validation, id=self.validation_menu.GetId())
        self.Bind(wx.EVT_MENU, self.on_3d_plot, id=self.plot_3d_menu.GetId())
        self.Bind(wx.EVT_MENU, self.on_interpolate_facies, id=self.interpolate_facies.GetId())

        self.Bind(wx.EVT_MENU, self.on_gr_vshale, id=self.gr_vshale_menu.GetId())

    # Virtual event handlers, override them in your derived class
    def new_project(self, event):
        event.Skip()

    def save_project(self, event):
        event.Skip()

    def open_project(self, event):
        event.Skip()

    def load_las_dlg(self, event):
        event.Skip()

    def plot_log(self, event):
        event.Skip()

    def correlation_plot(self, event):
        event.Skip()

    def overlay_plot(self, event):
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

    def on_3d_plot(self, event):
        event.Skip()

    def on_interpolate_facies(self, event):
        event.Skip()

    def on_gr_vshale(self, event):
        event.Skip()