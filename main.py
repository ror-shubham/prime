import wx
from readLas import ReadLas
from log_plot import PlotDemoApp
import numpy as np
import wx.lib.inspection
from well_select_dialog import SelectWellDialog
from cross_plot import SelectCrossPlotField, PlotCross

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
        lasObj.df = lasObj.df.replace(-999.2500, np.nan)
        # self.df = lasObj.df.replace(-999.2500, np.nan)
        # TODO handle nan values implicitly
        # self.df = self.df.replace(-999.2500, np.nan)
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
        selected = self.get_selected()
        num_selected = 0
        for val in selected.values():
            num_selected += len(val)
        if num_selected == 1:
            selected_key = list(selected.keys())[0]
            b = selected[selected_key]
            df = self.wells[selected_key][selected[selected_key][0]].df
            PlotDemoApp(df)
        # TODO add a dialogue if num_selected != 1

    def cross_plot(self, event):
        selected = self.get_selected()
        col_arr = []
        df_arr = []
        # TODO assumption here: only one LAS selected per well
        for k in selected.keys():
            if len(selected[k]) == 1:
                col_arr.append(self.wells[k][0].df.columns)
                df_arr.append(self.wells[k][0].df)
        # TODO assumption: at least one is selected
        common_fields = col_arr[0]
        for col in col_arr:
            common_fields = common_fields.intersection(col)
        dlg = SelectCrossPlotField(self, common_fields.tolist())
        dlg.SetSize(250, -1)
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val != wx.ID_OK:
            return
        choice_field = dlg.get_selection()
        PlotCross(df_arr, choice_field)


    def get_selected(self):
        self.selected_dict = {}
        for well_name in self.well_to_tree:
            print(well_name)
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
