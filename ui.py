# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"First frame", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.m_menubar1 = wx.MenuBar( 0 )
		self.file_menu = wx.Menu()
		self.exit_menu = wx.MenuItem( self.file_menu, wx.ID_EXIT, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.Append( self.exit_menu )

		self.m_menubar1.Append( self.file_menu, u"File" )

		self.las_menu = wx.Menu()
		self.load_menu = wx.MenuItem( self.las_menu, wx.ID_ANY, u"Load LAS", wx.EmptyString, wx.ITEM_NORMAL )
		self.las_menu.Append( self.load_menu )

		self.m_menubar1.Append( self.las_menu, u"LAS" )

		self.tools_menu = wx.Menu()
		self.plot_menu = wx.Menu()
		self.log_plot_menu = wx.MenuItem( self.plot_menu, wx.ID_ANY, u"Log Plot", wx.EmptyString, wx.ITEM_NORMAL )
		self.plot_menu.Append( self.log_plot_menu )
		self.log_plot_menu.Enable( False )

		self.cross_plot_menu = wx.MenuItem( self.plot_menu, wx.ID_ANY, u"Cross Plot", wx.EmptyString, wx.ITEM_NORMAL )
		self.plot_menu.Append( self.cross_plot_menu )

		self.tools_menu.AppendSubMenu( self.plot_menu, u"Plot" )

		self.m_menubar1.Append( self.tools_menu, u"Tools" )

		self.SetMenuBar( self.m_menubar1 )


		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.loadLas, id = self.load_menu.GetId() )
		self.Bind( wx.EVT_MENU, self.plot_log, id = self.log_plot_menu.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def loadLas( self, event ):
		event.Skip()

	def plot_log( self, event ):
		event.Skip()


