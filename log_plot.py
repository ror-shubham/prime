# -*- coding: utf-8 -*-
# pylint: disable=E1101, C0330, C0103
#   E1101: Module X has no Y member
#   C0330: Wrong continued indentation
#   C0103: Invalid attribute/variable/method name
"""
demo.py
=======

This is a demo showing some of the capabilities of the :mod:`wx.lib.plot`
package. It is intended to be run as a standalone script via::

  user@host:.../site-packages/wx/lib/plot$ python examples/demo.py

"""
__docformat__ = "restructuredtext en"

# Third Party
import wx
from wx.lib import plot as wxplot

from numpy import arange, sin, pi
import matplotlib

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.use('WXAgg')

# Needs NumPy
try:
    import numpy as np
except ImportError:
    msg = """
    This module requires the NumPy module, which could not be
    imported.  It probably is not installed (it's not part of the
    standard Python distribution). See the Numeric Python site
    (http://numpy.scipy.org) for information on downloading source or
    binaries, or just try `pip install numpy` and it will probably
    work."""
    raise ImportError("NumPy not found.\n" + msg)


# ---------------------------------------------------------------------------
### Drawing Functions
# ---------------------------------------------------------------------------
def _draw1Objects(data):
    depth = data.index.to_numpy()
    data2 = np.flip(np.column_stack((data[data.columns[1]].to_numpy(), depth)), 0)
    lines = wxplot.PolySpline(data2, legend='Red Line', colour='red')

    return wxplot.PlotGraphics([lines],
                               "Graph Title",
                               data.columns.values[1],
                               "Depth",
                               )


# ---------------------------------------------------------------------------
### Demo Application
# ---------------------------------------------------------------------------
class PlotDemoApp(object):
    def __init__(self, data):
        self.app = wx.App()
        self.frame = PlotDemoMainFrame(None, -1, "PlotCanvas", data)
        panel = CanvasPanel(self.frame)
        panel.draw()
        self.frame.Show(True)
        self.app.MainLoop()

class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

    def draw(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        self.axes.plot(t, s)

class PlotDemoMainFrame(wx.Frame):
    # -----------------------------------------------------------------------
    ### UI Initialization
    # -----------------------------------------------------------------------
    def __init__(self, parent, wxid, title, data):
        wx.Frame.__init__(self, parent, wxid, title,
                          wx.DefaultPosition, (800, 600))


        # Now Create the menu bar and items
        self.mainmenu = wx.MenuBar()

        self._init_file_menu()
        self._init_plot_menu()
        self._init_options_menu()
        self._init_help_menu()

        self.SetMenuBar(self.mainmenu)

        # A status bar to tell people what's happening
        self.CreateStatusBar(1)

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)

        self.client = FigureCanvas(self, -1, self.figure)
        # define the function for drawing pointLabels
#        self.client.SetPointLabelFunc(self.DrawPointLabel)
        self.client.pointLabelFunc = self.DrawPointLabel
        # Create mouse event for showing cursor coords in status bar
        self.client.canvas.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        # Show closest point when enabled
        self.client.canvas.Bind(wx.EVT_MOTION, self.OnMotion)
        self.client.Draw(_draw1Objects(data.dropna()))

    def _init_file_menu(self):
        """ Create the "File" menu items. """
        menu = wx.Menu()
        menu.Append(200, 'Page Setup...', 'Setup the printer page')
        self.Bind(wx.EVT_MENU, self.OnFilePageSetup, id=200)
        menu.Append(201, 'Print Preview...', 'Show the current plot on page')
        self.Bind(wx.EVT_MENU, self.OnFilePrintPreview, id=201)
        menu.Append(202, 'Print...', 'Print the current plot')
        self.Bind(wx.EVT_MENU, self.OnFilePrint, id=202)
        menu.Append(203, 'Save Plot...', 'Save current plot')
        self.Bind(wx.EVT_MENU, self.OnSaveFile, id=203)
        menu.Append(205, 'E&xit', 'Enough of this already!')
        self.Bind(wx.EVT_MENU, self.OnFileExit, id=205)
        self.mainmenu.Append(menu, '&File')

    def _init_plot_menu(self):
        """ Create the "Plot" menu items. """
        menu = wx.Menu()

        menu.Append(211, '&Redraw', 'Redraw plots')
        self.Bind(wx.EVT_MENU, self.OnPlotRedraw, id=211)
        menu.Append(212, '&Clear', 'Clear canvas')
        self.Bind(wx.EVT_MENU, self.OnPlotClear, id=212)
        menu.Append(213, '&Scale', 'Scale canvas')
        self.Bind(wx.EVT_MENU, self.OnPlotScale, id=213)

        menu.AppendSeparator()

        menu.Append(225, 'Scroll Up 1', 'Move View Up 1 Unit')
        self.Bind(wx.EVT_MENU, self.OnScrUp, id=225)
        menu.Append(230, 'Scroll Rt 2', 'Move View Right 2 Units')
        self.Bind(wx.EVT_MENU, self.OnScrRt, id=230)
        menu.Append(235, '&Plot Reset', 'Reset to original plot')
        self.Bind(wx.EVT_MENU, self.OnReset, id=235)

        self.mainmenu.Append(menu, '&Plot')


    def _init_options_menu(self):
        """ Create the "Options" menu items. """
        menu = wx.Menu()

        menu.Append(214, 'Enable &Zoom',
                    'Enable Mouse Zoom', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnableZoom, id=214)
        menu.Check(214, True)

        menu.Append(217, 'Enable &Drag',
                    'Activates dragging mode', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnableDrag, id=217)

        menu.Append(222, 'Enable &Point Label',
                    'Show Closest Point', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnablePointLabel, id=222)

        menu.Append(223, 'Enable &Anti-Aliasing',
                    'Smooth output', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnableAntiAliasing, id=223)

        menu.Append(224, 'Enable &High-Resolution AA',
                    'Draw in higher resolution', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnableHiRes, id=224)

        menu.AppendSeparator()

        menu.Append(226, 'Enable Center Lines',
                    'Draw center lines', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnableCenterLines, id=226)

        menu.Append(227, 'Enable Diagonal Lines',
                    'Draw diagonal lines', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnableDiagonals, id=227)

        menu.Append(220, 'Enable &Legend',
                    'Turn on Legend', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnableLegend, id=220)

        ### SubMenu for Grid
        submenu = wx.Menu()
        self.gridSubMenu = submenu

        submenu.AppendCheckItem(2151, "X Gridlines", "Enable X gridlines")
        submenu.AppendCheckItem(2152, "Y Gridlines", "Enable Y gridlines")
        submenu.AppendCheckItem(2153, "All Gridlines", "Enable All gridlines")
        submenu.Check(2151, True)
        submenu.Check(2152, True)
        submenu.Check(2153, True)

        self.Bind(wx.EVT_MENU, self.OnEnableGridX, id=2151)
        self.Bind(wx.EVT_MENU, self.OnEnableGridY, id=2152)
        self.Bind(wx.EVT_MENU, self.OnEnableGridAll, id=2153)

        menu.Append(215, 'Enable Grid', submenu, 'Turn on Grid')

        ### SubMenu for Axes
        submenu = wx.Menu()
        submenu_items = ("Bottom", "Left", "Top", "Right",
                         "Bottom+Left", "All")
        self.axesSubMenu = submenu
        for _i, item in enumerate(submenu_items, 2401):
            submenu.AppendCheckItem(_i, item, "Enables {} axis".format(item))
            submenu.Check(_i, True)

        self.Bind(wx.EVT_MENU, self.OnEnableAxesBottom, id=2401)
        self.Bind(wx.EVT_MENU, self.OnEnableAxesLeft, id=2402)
        self.Bind(wx.EVT_MENU, self.OnEnableAxesTop, id=2403)
        self.Bind(wx.EVT_MENU, self.OnEnableAxesRight, id=2404)
        self.Bind(wx.EVT_MENU, self.OnEnableAxesBottomLeft, id=2405)
        self.Bind(wx.EVT_MENU, self.OnEnableAxesAll, id=2406)

        menu.Append(240, 'Enable Axes', submenu,
                    'Enables the display of the Axes')

        submenu = wx.Menu()
        submenu_items = ("Bottom", "Left", "Top", "Right")
        help_txt = "Enables {} axis values"
        self.axesValuesSubMenu = submenu
        for _i, item in enumerate(submenu_items, 2451):
            submenu.AppendCheckItem(_i, item, help_txt.format(item))

        submenu.Check(2451, True)
        submenu.Check(2452, True)
        submenu.Check(2453, False)
        submenu.Check(2454, False)

        self.Bind(wx.EVT_MENU, self.OnEnableAxesValuesBottom, id=2451)
        self.Bind(wx.EVT_MENU, self.OnEnableAxesValuesLeft, id=2452)
        self.Bind(wx.EVT_MENU, self.OnEnableAxesValuesTop, id=2453)
        self.Bind(wx.EVT_MENU, self.OnEnableAxesValuesRight, id=2454)

        menu.Append(245, 'Enable Axes Values', submenu,
                    'Enables the display of the axes values')

        submenu = wx.Menu()
        submenu_items = ("Bottom", "Left", "Top", "Right",
                         "Bottom+Left", "All")
        help_txt = "Enables {} ticks"
        self.ticksSubMenu = submenu
        for _i, item in enumerate(submenu_items, 2501):
            submenu.AppendCheckItem(_i, item, help_txt.format(item))

        submenu.Check(2501, False)
        submenu.Check(2502, False)
        submenu.Check(2503, False)
        submenu.Check(2504, False)

        self.Bind(wx.EVT_MENU, self.OnEnableTicksBottom, id=2501)
        self.Bind(wx.EVT_MENU, self.OnEnableTicksLeft, id=2502)
        self.Bind(wx.EVT_MENU, self.OnEnableTicksTop, id=2503)
        self.Bind(wx.EVT_MENU, self.OnEnableTicksRight, id=2504)
        self.Bind(wx.EVT_MENU, self.OnEnableTicksBottomLeft, id=2505)
        self.Bind(wx.EVT_MENU, self.OnEnableTicksAll, id=2506)

        menu.Append(250, 'Enable Ticks', submenu,
                    'Enables the display of the ticks')

        menu.Append(255, 'Enable Plot Title',
                    'Enables the plot title', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnablePlotTitle, id=255)
        menu.Check(255, True)

        menu.Append(270, 'Enable Axes Labels',
                    'Enables the X and Y axes labels', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnEnableAxesLabels, id=270)
        menu.Check(270, True)

        menu.Append(271, 'Enable Log-Y',
                    'Changes the Y axis to log10 scale', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnLogY, id=271)
        menu.Append(272, 'Enable Log-X',
                    'Changes the X axis to log10 scale', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnLogX, id=272)

        menu.Append(273, 'Enable Abs(X)',
                    'Applies absolute value transform to X axis',
                    kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnAbsX, id=273)
        menu.Append(274, 'Enable Abs(Y)',
                    'Applies absolute value transform to Y axis',
                    kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU, self.OnAbsY, id=274)

        menu.AppendSeparator()

        menu.Append(231, 'Set Gray Background',
                    'Change background colour to gray')
        self.Bind(wx.EVT_MENU, self.OnBackgroundGray, id=231)
        menu.Append(232, 'Set &White Background',
                    'Change background colour to white')
        self.Bind(wx.EVT_MENU, self.OnBackgroundWhite, id=232)
        menu.Append(233, 'Set Red Label Text',
                    'Change label text colour to red')
        self.Bind(wx.EVT_MENU, self.OnForegroundRed, id=233)
        menu.Append(234, 'Set &Black Label Text',
                    'Change label text colour to black')
        self.Bind(wx.EVT_MENU, self.OnForegroundBlack, id=234)

        self.mainmenu.Append(menu, '&Options')

        self.plot_options_menu = menu

    def _init_help_menu(self):
        """ Create the "Help" menu items. """
        menu = wx.Menu()
        menu.Append(300, '&About', 'About this thing...')
        self.Bind(wx.EVT_MENU, self.OnHelpAbout, id=300)
        self.mainmenu.Append(menu, '&Help')

    # -----------------------------------------------------------------------
    ### Event Handling
    # -----------------------------------------------------------------------


    def OnMouseLeftDown(self, event):
        s = "Left Mouse Down at Point: (%.4f, %.4f)" % self.client.GetXY(
            event)
        self.SetStatusText(s)
        event.Skip()  # allows plotCanvas OnMouseLeftDown to be called

    def OnMotion(self, event):
        # show closest point (when enbled)
        if self.client.enablePointLabel:
            # make up dict with info for the pointLabel
            # I've decided to mark the closest point on the closest curve
            dlst = self.client.GetClosestPoint(
                self.client.GetXY(event),
                pointScaled=True,
            )
            if dlst != []:  # returns [] if none
                curveNum, legend, pIndex, pointXY, scaledXY, distance = dlst
                # make up dictionary to pass to my user function (see
                # DrawPointLabel)
                mDataDict = {"curveNum": curveNum,
                             "legend": legend,
                             "pIndex": pIndex,
                             "pointXY": pointXY,
                             "scaledXY": scaledXY}
                # pass dict to update the pointLabel
                self.client.UpdatePointLabel(mDataDict)
        event.Skip()  # go to next handler

    def OnFilePageSetup(self, event):
        self.client.PageSetup()

    def OnFilePrintPreview(self, event):
        self.client.PrintPreview()

    def OnFilePrint(self, event):
        self.client.Printout()

    def OnSaveFile(self, event):
        self.client.SaveFile()

    def OnFileExit(self, event):
        self.Close()


    # -----------------------------------------------------------------------
    ### PlotDraw Events
    # -----------------------------------------------------------------------

    def OnPlotRedraw(self, event):
        self.client.Redraw()

    def OnPlotClear(self, event):
        self.client.Clear()

    def OnPlotScale(self, event):
        if self.client.last_draw is not None:
            graphics, xAxis, yAxis = self.client.last_draw
            self.client.Draw(graphics, (1, 3.05), (0, 1))

    # -----------------------------------------------------------------------
    ### Other Events
    # -----------------------------------------------------------------------
    def OnScrUp(self, event):
        self.client.ScrollUp(1)

    def OnScrRt(self, event):
        self.client.ScrollRight(2)

    def OnReset(self, event):
        self.client.Reset()

    def OnHelpAbout(self, event):
        from wx.lib.dialogs import ScrolledMessageDialog
        about = ScrolledMessageDialog(self, __doc__, "About...")
        about.ShowModal()

    def OnBackgroundGray(self, event):
        self.client.SetBackgroundColour("#CCCCCC")
        self.client.Redraw()

    def OnBackgroundWhite(self, event):
        self.client.SetBackgroundColour("white")
        self.client.Redraw()

    def OnForegroundRed(self, event):
        self.client.SetForegroundColour("red")
        self.client.Redraw()

    def OnForegroundBlack(self, event):
        self.client.SetForegroundColour("black")
        self.client.Redraw()

    # -----------------------------------------------------------------------
    ### Enable Grid Events
    # -----------------------------------------------------------------------
    def _checkOtherGridMenuItems(self):
        """ check or uncheck the submenu items """
        self.gridSubMenu.Check(2151, self.client.enableGrid[0])
        self.gridSubMenu.Check(2152, self.client.enableGrid[1])
        self.gridSubMenu.Check(2153, all(self.client.enableGrid))

    def OnEnableGridX(self, event):
        old = self.client.enableGrid
        self.client.enableGrid = (event.IsChecked(), old[1])
        self._checkOtherGridMenuItems()

    def OnEnableGridY(self, event):
        old = self.client.enableGrid
        self.client.enableGrid = (old[0], event.IsChecked())
        self._checkOtherGridMenuItems()

    def OnEnableGridAll(self, event):
        self.client.enableGrid = event.IsChecked()
        self._checkOtherGridMenuItems()
        self.gridSubMenu.Check(2151, event.IsChecked())
        self.gridSubMenu.Check(2152, event.IsChecked())

    # -----------------------------------------------------------------------
    ### Enable Axes Events
    # -----------------------------------------------------------------------
    def _checkOtherAxesMenuItems(self):
        """ check or uncheck the submenu items """
        self.axesSubMenu.Check(2401, self.client.enableAxes[0])
        self.axesSubMenu.Check(2402, self.client.enableAxes[1])
        self.axesSubMenu.Check(2403, self.client.enableAxes[2])
        self.axesSubMenu.Check(2404, self.client.enableAxes[3])
        self.axesSubMenu.Check(2405, all(self.client.enableAxes[:2]))
        self.axesSubMenu.Check(2406, all(self.client.enableAxes))

    def OnEnableAxesBottom(self, event):
        old = self.client.enableAxes
        self.client.enableAxes = (event.IsChecked(), old[1], old[2], old[3])
        self._checkOtherAxesMenuItems()

    def OnEnableAxesLeft(self, event):
        old = self.client.enableAxes
        self.client.enableAxes = (old[0], event.IsChecked(), old[2], old[3])
        self._checkOtherAxesMenuItems()

    def OnEnableAxesTop(self, event):
        old = self.client.enableAxes
        self.client.enableAxes = (old[0], old[1], event.IsChecked(), old[3])
        self._checkOtherAxesMenuItems()

    def OnEnableAxesRight(self, event):
        old = self.client.enableAxes
        self.client.enableAxes = (old[0], old[1], old[2], event.IsChecked())
        self._checkOtherAxesMenuItems()

    def OnEnableAxesBottomLeft(self, event):
        checked = event.IsChecked()
        old = self.client.enableAxes
        self.client.enableAxes = (checked, checked, old[2], old[3])
        self._checkOtherAxesMenuItems()

    def OnEnableAxesAll(self, event):
        checked = event.IsChecked()
        self.client.enableAxes = (checked, checked, checked, checked)
        self._checkOtherAxesMenuItems()

    # -----------------------------------------------------------------------
    ### Enable Ticks Events
    # -----------------------------------------------------------------------
    def _checkOtherTicksMenuItems(self):
        """ check or uncheck the submenu items """
        self.ticksSubMenu.Check(2501, self.client.enableTicks[0])
        self.ticksSubMenu.Check(2502, self.client.enableTicks[1])
        self.ticksSubMenu.Check(2503, self.client.enableTicks[2])
        self.ticksSubMenu.Check(2504, self.client.enableTicks[3])
        self.ticksSubMenu.Check(2505, all(self.client.enableTicks[:2]))
        self.ticksSubMenu.Check(2506, all(self.client.enableTicks))

    def OnEnableTicksBottom(self, event):
        old = self.client.enableTicks
        self.client.enableTicks = (event.IsChecked(), old[1],
                                   old[2], old[3])
        self._checkOtherTicksMenuItems()

    def OnEnableTicksLeft(self, event):
        old = self.client.enableTicks
        self.client.enableTicks = (old[0], event.IsChecked(),
                                   old[2], old[3])
        self._checkOtherTicksMenuItems()

    def OnEnableTicksTop(self, event):
        old = self.client.enableTicks
        self.client.enableTicks = (old[0], old[1],
                                   event.IsChecked(), old[3])
        self._checkOtherTicksMenuItems()

    def OnEnableTicksRight(self, event):
        old = self.client.enableTicks
        self.client.enableTicks = (old[0], old[1],
                                   old[2], event.IsChecked())
        self._checkOtherTicksMenuItems()

    def OnEnableTicksBottomLeft(self, event):
        checked = event.IsChecked()
        old = self.client.enableTicks
        self.client.enableTicks = (checked, checked, old[2], old[3])
        self._checkOtherTicksMenuItems()

    def OnEnableTicksAll(self, event):
        checked = event.IsChecked()
        self.client.enableTicks = tuple([checked] * 4)
        self._checkOtherTicksMenuItems()

    # -----------------------------------------------------------------------
    ### Enable AxesValues Events
    # -----------------------------------------------------------------------
    def OnEnableAxesValuesBottom(self, event):
        old = self.client.enableAxesValues
        self.client.enableAxesValues = (event.IsChecked(), old[1],
                                        old[2], old[3])

    def OnEnableAxesValuesLeft(self, event):
        old = self.client.enableAxesValues
        self.client.enableAxesValues = (old[0], event.IsChecked(),
                                        old[2], old[3])

    def OnEnableAxesValuesTop(self, event):
        old = self.client.enableAxesValues
        self.client.enableAxesValues = (old[0], old[1],
                                        event.IsChecked(), old[3])

    def OnEnableAxesValuesRight(self, event):
        old = self.client.enableAxesValues
        self.client.enableAxesValues = (old[0], old[1],
                                        old[2], event.IsChecked())

    # -----------------------------------------------------------------------
    ### Other Enable Events
    # -----------------------------------------------------------------------
    def OnEnableZoom(self, event):
        self.client.enableZoom = event.IsChecked()
        if self.mainmenu.IsChecked(217):
            self.mainmenu.Check(217, False)

    def OnEnableDrag(self, event):
        self.client.enableDrag = event.IsChecked()
        if self.mainmenu.IsChecked(214):
            self.mainmenu.Check(214, False)

    def OnEnableLegend(self, event):
        self.client.enableLegend = event.IsChecked()

    def OnEnablePointLabel(self, event):
        self.client.enablePointLabel = event.IsChecked()

    def OnEnableAntiAliasing(self, event):
        self.client.enableAntiAliasing = event.IsChecked()

    def OnEnableHiRes(self, event):
        self.client.enableHiRes = event.IsChecked()

    def OnEnablePlotTitle(self, event):
        self.client.enablePlotTitle = event.IsChecked()

    def OnEnableAxesLabels(self, event):
        self.client.enableAxesLabels = event.IsChecked()

    def OnEnableCenterLines(self, event):
        self.client.enableCenterLines = event.IsChecked()

    def OnEnableDiagonals(self, event):
        self.client.enableDiagonals = event.IsChecked()

    def OnLogX(self, event):
        self.client.logScale = (event.IsChecked(), self.client.logScale[1])
        self.client.Redraw()

    def OnLogY(self, event):
        self.client.logScale = (self.client.logScale[0], event.IsChecked())
        self.client.Redraw()

    def OnAbsX(self, event):
        self.client.absScale = (event.IsChecked(), self.client.absScale[1])
        self.client.Redraw()

    def OnAbsY(self, event):
        self.client.absScale = (self.client.absScale[0], event.IsChecked())
        self.client.Redraw()

    def resetDefaults(self):
        """Just to reset the fonts back to the PlotCanvas defaults"""
        self.client.SetFont(wx.Font(10,
                                    wx.FONTFAMILY_SWISS,
                                    wx.FONTSTYLE_NORMAL,
                                    wx.FONTWEIGHT_NORMAL)
                            )
        self.client.fontSizeAxis = 10
        self.client.fontSizeLegend = 7
        self.client.logScale = (False, False)
        self.client.xSpec = 'auto'
        self.client.ySpec = 'auto'

    def DrawPointLabel(self, dc, mDataDict):
        """
        This is the fuction that defines how the pointLabels are plotted

        :param dc: DC that will be passed
        :param mDataDict: Dictionary of data that you want to use
                          for the pointLabel

        As an example I have decided I want a box at the curve point
        with some text information about the curve plotted below.
        Any wxDC method can be used.

        """
        dc.SetPen(wx.Pen(wx.BLACK))
        dc.SetBrush(wx.Brush(wx.BLACK, wx.BRUSHSTYLE_SOLID))

        sx, sy = mDataDict["scaledXY"]  # scaled x,y of closest point
        # 10by10 square centered on point
        dc.DrawRectangle(sx - 5, sy - 5, 10, 10)
        px, py = mDataDict["pointXY"]
        cNum = mDataDict["curveNum"]
        pntIn = mDataDict["pIndex"]
        legend = mDataDict["legend"]
        # make a string to display
        s = "Crv# %i, '%s', Pt. (%.2f,%.2f), PtInd %i" % (
            cNum, legend, px, py, pntIn)
        dc.DrawText(s, sx, sy + 1)


def run_demo():
    """
    Run the :mod:`wx.lib.plot` demo application.
    """
    PlotDemoApp()


if __name__ == '__main__':
    run_demo()
