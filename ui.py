import wx
import wx.xrc


class MainFrame(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"First frame", pos=wx.DefaultPosition, size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
		self.box_main = wx.BoxSizer(wx.VERTICAL)

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
		self.log_plot_menu.Enable(False)

		self.cross_plot_menu = wx.MenuItem(self.plot_menu, wx.ID_ANY, u"Cross Plot")
		self.plot_menu.Append(self.cross_plot_menu)

		self.tools_menu.AppendSubMenu(self.plot_menu, u"Plot")

		self.menubar.Append(self.tools_menu, u"Tools")

		self.SetMenuBar(self.menubar)

		self.Centre(wx.BOTH)
		self.Maximize()

		# Connect Events
		self.Bind(wx.EVT_MENU, self.load_las, id=self.load_menu.GetId())
		self.Bind(wx.EVT_MENU, self.plot_log, id=self.log_plot_menu.GetId())

		def __del__(self):
			pass

		# Virtual event handlers, overide them in your derived class
		def load_las(self, event):
			event.Skip()

		def plot_log(self, event):
			event.Skip()
