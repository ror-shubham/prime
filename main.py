import wx
from readLas import ReadLas
from log_plot import PlotDemoApp
import numpy as np
import wx.lib.inspection
from well_select_dialog import SelectWellDialog
from prediction_ui import PredictionDialog
from validation_ui import ValidationDialog
from cross_plot import SelectCrossPlotField, PlotCross
from ml import karnal
from sklearn.ensemble import RandomForestRegressor

import ui


class Frame(ui.MainFrame):
    def __init__(self, parent):
        ui.MainFrame.__init__(self, parent)
        # in form of {wellId: [las1, ...]}
        self.wells = {}
        self.well_to_tree = {}
        self.selected_dict = {}
        self.selected_df_list = []

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
        num_selected = len(selected)
        if num_selected == 1:
            df = selected[0]
            PlotDemoApp(df)
        # TODO add a dialogue if num_selected != 1

    def cross_plot(self, event):

        # TODO assumption here: only one LAS selected per well

        # TODO assumption: at least one is selected
        common_fields = self._get_common_fields()
        dlg = SelectCrossPlotField(self, common_fields)
        dlg.SetSize(250, -1)
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val != wx.ID_OK:
            return
        choice_field = dlg.get_selection()
        df_arr = self.get_selected()
        PlotCross(df_arr, choice_field)

    def _get_common_fields(self):
        col_arr = []
        selected_list = self.get_selected()
        for selected in selected_list:
            col_arr.append(selected.columns)
        common_fields = col_arr[0]
        for col in col_arr:
            common_fields = common_fields.intersection(col)
        return common_fields.tolist()

    def get_selected(self):
        self.selected_df_list = []
        self.selected_dict = {}
        for well_name in self.well_to_tree:
            tree = self.well_to_tree[well_name]
            children = tree.GetChildren()
            for index, child in enumerate(children):
                if child.IsChecked():
                    self.selected_df_list.append(self.wells[well_name][index].df)
                    if well_name in self.selected_dict:
                        if index not in self.selected_dict[well_name]:
                            self.selected_dict[well_name].append(index)
                    else:
                        self.selected_dict[well_name] = [index]
        return self.selected_df_list

    def on_prediction(self, event):
        common_fields = self._get_common_fields()
        dlg2 = PredictionDialog(self, common_fields)
        val2 = dlg2.ShowModal()
        selected = self.get_selected()
        a =  karnal.prediction(selected, 'BS', 12, RandomForestRegressor)
        c = 1

        # TODO run prediction here

    def on_validation(self, event):
        common_fields = self._get_common_fields()
        dlg2 = ValidationDialog(self, common_fields)
        val2 = dlg2.ShowModal()
        selected = self.get_selected()
        a = karnal.validation(selected, 'BS', RandomForestRegressor, 'r2')
        print(a)
        # TODO run prediction here


if __name__ == "__main__":
    app = wx.App(False)
    frame = Frame(None)
    frame.Show(True)
    app.MainLoop()
