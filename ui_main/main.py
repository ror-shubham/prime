import pickle

import wx
from utils.readLas import ReadLas
from plots.log_plot import PlotDemoApp
import numpy as np
import wx.lib.inspection
from plots.cross_plot import SelectCrossPlotField, PlotCross
from ml import main
from sklearn.ensemble import RandomForestRegressor

from ui_main import main_ui

from ui_main.las.load_las.well_select_dialog import SelectWellDialog
from ui_main.tools.interpolate.prediction.prediction_dialog import PredictionDialog
from ui_main.tools.interpolate.validation.validation_dialog import ValidationDialog
from ui_main.file.new_project import NewProjectDialog
from ui_main.file.open_project import open_project_dlg
from ui_main.initial_dialog import InitialDialog
from ui_main.file.save_project import save_project_to_file

import matplotlib as mpl
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar


class Frame(main_ui.MainFrame):
    def __init__(self, parent, project_path):
        self.wells = {}
        self.well_to_tree = {}
        self.selected_dict = {}
        self.selected_df_list = []
        self.project_name = ''
        self.project_path = project_path

        main_ui.MainFrame.__init__(self, parent, project_path)
        # read the project file first
        with open(project_path, 'rb') as f:
            well_path_dict = pickle.load(f)
        for well_name in well_path_dict:
            for path in well_path_dict[well_name]:
                self.load_las_logic(path, well_name)

    def load_las_dlg(self, event):
        dlg = SelectWellDialog(self, list(self.wells.keys()))
        dlg.SetSize(250,-1)
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val != wx.ID_OK:
            return
        well_name = dlg.get_well_name()
        openFileDialog = wx.FileDialog(self, "Open", "", "",
                                       "LAS files (*.las)|*.las",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        path = openFileDialog.GetPath()
        self.load_las_logic(path, well_name)

    def load_las_logic(self, path, well_name):
        lasObj = ReadLas(path)
        lasObj.df = lasObj.df.replace(-999.2500, np.nan)
        # self.df = lasObj.df.replace(-999.2500, np.nan)
        # TODO handle nan values implicitly
        # self.df = self.df.replace(-999.2500, np.nan)
        if well_name in self.wells:
            self.wells[well_name].append(lasObj)
            child_tree = self.well_to_tree[well_name]
            beg = lasObj.get_begin_depth()
            end = lasObj.get_end_depth()
            self.add_las_to_well(child_tree, str(beg) + " - " + str(end))
            self.left_tree.ExpandAll()

        else:
            self.wells[well_name] = [lasObj]
            child_tree = self.add_well(self.root, well_name)
            self.well_to_tree[well_name] = child_tree
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
        self.predicted_df =  main.prediction(selected, 'CALI', 22, RandomForestRegressor)
        a=1

        # TODO run prediction here

    def on_validation(self, event):
        common_fields = self._get_common_fields()
        dlg2 = ValidationDialog(self, common_fields)
        val2 = dlg2.ShowModal()
        selected = self.get_selected()
        a = main.validation(selected, 'BS', RandomForestRegressor, 'r2')
        print(a)
        # TODO run prediction here

    def new_project(self, event):
        dlg = NewProjectDialog(self)
        dlg.SetSize(450, 80)
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val != wx.ID_OK:
            return
        # name = os.path.basename(path)
        # self.project_name = name
        # self.project_path = path

    def open_project(self, event):
        open_project_dlg(self)

    def save_project(self, event):
        wells_modified = {k: list(map(lambda x: x.read_path, v)) for k, v in self.wells.items()}
        save_project_to_file(wells_modified, self.project_path)

    def on_3d_plot(self, event):
        from numpy import arange, sin, pi
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        self.figure = mpl.figure.Figure()
        self.canvas_main = FigureCanvas(self.panel_right, -1, self.figure)
        self.box_right.Add(self.canvas_main, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.axes_figure = self.figure.add_subplot(111)
        self.axes_figure.plot(t, s)
        self.box_right.Layout()


if __name__ == "__main__":
    app = wx.App(False)
    dlg = InitialDialog(None)
    dlg.ShowModal()
    project_path = dlg.get_project_path()

    frame = Frame(None, project_path)
    frame.Show(True)
    wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
