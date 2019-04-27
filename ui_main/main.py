import pickle

import wx
from utils.readLas import ReadLas
from plots.log_plot import PlotLog
import numpy as np
import wx.lib.inspection
from plots.cross_plot import SelectCrossPlotField, PlotCross
from plots.plot_3d import plot_3d
from ml import main
from sklearn.ensemble import RandomForestRegressor

from ui_main import ui
from ui_main.las.load_las.well_select_dialog import SelectWellDialog
from ui_main.tools.interpolate.prediction.prediction_dialog import PredictionDialog
from ui_main.tools.interpolate.validation.validation_dialog import ValidationDialog
from ui_main.file.new_project import NewProjectDialog
from ui_main.file.open_project import open_project_dlg
from ui_main.initial_dialog import InitialDialog
from ui_main.file.save_project import save_project_to_file
from ui_main.plot_notebook import PlotNotebook

from utils.commons import show_message_dialog

from cefpython3 import cefpython as cef



class Frame(ui.MainFrame):
    def __init__(self, parent, project_path):
        self.wells = {}
        self.well_to_tree = {}
        self.selected_dict = {}
        self.selected_df_list = []
        self.project_name = ''
        self.project_path = project_path

        ui.MainFrame.__init__(self, parent, project_path)
        # read the project file first
        try:
            with open(project_path, 'rb') as f:
                well_path_dict = pickle.load(f)
            for well_name in well_path_dict:
                for path in well_path_dict[well_name]:
                    self.load_las_logic(path, well_name)
        except:
            print('Error reading project data')

        self.plotter = PlotNotebook(self.panel_right)
        self.box_right.Add(self.plotter, 1, wx.EXPAND)

    def load_las_dlg(self, event):
        dlg = SelectWellDialog(self, list(self.wells.keys()))
        dlg.SetSize(250, -1)
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
        # TODO handle nan values implicitly, here it's hard coded
        if well_name in self.wells:
            self.wells[well_name].append(lasObj)
            child_tree = self.well_to_tree[well_name]
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
        selected = self.get_selected_df_list()
        num_selected = len(selected)
        if num_selected == 1:
            df = selected[0]
            PlotLog(self.panel_right, self.plotter, df)
        else:
            show_message_dialog(self, 'Only one well should be selected for Log Plot',
                                'Error', )

    def cross_plot(self, event):

        # TODO assumption here: only one LAS selected per well

        df_arr = self.get_selected_df_list()
        if (len(df_arr) < 2):
            show_message_dialog(self,
                                'At least two wells needs to be selected for Cross Plot',
                                'Error',)
        else:
            common_fields = self._get_common_fields()
            dlg = SelectCrossPlotField(self, common_fields)
            dlg.SetSize(250, -1)
            dlg.CenterOnScreen()
            val = dlg.ShowModal()
            if val != wx.ID_OK:
                return
            choice_field = dlg.get_selection()
            PlotCross(self.panel_right, self.plotter, df_arr, choice_field)

    def _get_common_fields(self):
        col_arr = []
        selected_list = self.get_selected_df_list()
        for selected in selected_list:
            col_arr.append(selected.columns)
        common_fields = col_arr[0]
        for col in col_arr:
            common_fields = common_fields.intersection(col)
        common_list = common_fields.tolist()
        common_list.remove('lat')
        common_list.remove('long')
        return common_list

    def get_selected_df_list(self):
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
        dlg = PredictionDialog(self, common_fields)
        modal_val = dlg.ShowModal()
        if modal_val != wx.ID_OK:
            return
        selected_prop = dlg.get_selected_property()
        selected_method = dlg.get_selected_method()
        num_wells = int(dlg.get_num_wells())
        selected_df_list = self.get_selected_df_list()
        self.predicted_df = main.prediction(selected_df_list, selected_prop, num_wells, RandomForestRegressor)

        # TODO run prediction here

    def on_validation(self, event):
        common_fields = self._get_common_fields()
        dlg = ValidationDialog(self, common_fields)
        modal_val = dlg.ShowModal()
        if modal_val != wx.ID_OK:
            return
        selected_prop = dlg.get_selected_property()
        selected_method = dlg.get_selected_method()
        selected_scoring = dlg.get_selected_scoring()
        selected_df_list = self.get_selected_df_list()
        scores = main.validation(selected_df_list, selected_prop, RandomForestRegressor, selected_scoring)
        show_message_dialog(self, scores, 'Scores')

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
        try:
            plot_3d(self.plotter, self.predicted_df)
        except AttributeError:
            show_message_dialog(self, 'Please run prediction first. Currently, 3d '
                                      'plot runs only in conjecture of prediction', 'Error')

def on_timer(_):
    cef.MessageLoopWork()



if __name__ == "__main__":
    app = wx.App(False)
    dlg = InitialDialog(None)
    val = dlg.ShowModal()
    if val == wx.ID_OK:
        project_path = dlg.get_project_path()
        frame = Frame(None, project_path)
        timer = wx.Timer(frame, 1)
        frame.Bind(wx.EVT_TIMER, on_timer, timer)
        timer.Start(10)  # 10ms timer
        frame.Show(True)
        wx.lib.inspection.InspectionTool().Show()
        app.MainLoop()
