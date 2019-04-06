import wx
from readLas import ReadLas
from log_plot import PlotDemoApp
import numpy as np
import wx.lib.inspection
from well_select_dialog import SelectWellDialog

import ui


class Frame(ui.MainFrame):
    def __init__(self, parent):
        ui.MainFrame.__init__(self, parent)
        # in form of {wellId: [las1, ...]}
        self.wells = {}
        self.well_to_tree = {}
        self.selected_dict = {}

    def load_las(self, event):
        dlg = SelectWellDialog(self, list(self.wells.keys()))
        dlg.SetSize(250,-1)
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val != wx.ID_OK:
            return
        selected = dlg.get_selection()
        openFileDialog = wx.FileDialog(self, "Open", "", "",
                                       "LAS files (*.las)|*.las",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        path = openFileDialog.GetPath()

        lasObj = ReadLas(path)
        self.df = lasObj.df
        # TODO handle nan values implicitly
        self.df = self.df.replace(-999.2500, np.nan)
        if selected in self.wells:
            self.wells[selected].append(lasObj)
            child_tree = self.well_to_tree[selected]
            beg = lasObj.get_begin_depth()
            end = lasObj.get_end_depth()
            self.add_las_to_well(child_tree, str(beg) + " - " + str(end))
            self.left_tree.ExpandAll()

        else:
            self.wells[selected] = [lasObj]
            child_tree = self.add_well(self.root, selected)
            self.well_to_tree[selected] = child_tree
            beg = lasObj.get_begin_depth()
            end = lasObj.get_end_depth()
            self.add_las_to_well(child_tree, str(beg) + " - " + str(end))
            self.left_tree.ExpandAll()
        self.log_plot_menu.Enable(True)

    def plot_log(self, event):
        PlotDemoApp(self.df)

    def cross_plot(self, event):
        self.get_selected()
        print(self.get_selected())

    def get_selected(self):
        for well_name in self.well_to_tree:
            tree = self.well_to_tree[well_name]
            children = tree.GetChildren()
            for index, child in enumerate(children):
                if child.IsChecked():
                    if well_name in self.selected_dict:
                        if index not in self.selected_dict[well_name]:
                            self.selected_dict[well_name].append(index)
                    else:
                        self.selected_dict[well_name] = [index]
            return self.selected_dict

if __name__ == "__main__":
    app = wx.App(False)
    frame = Frame(None)
    frame.Show(True)
    app.MainLoop()
