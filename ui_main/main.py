import pickle
from cefpython3 import cefpython as cef
import ntpath

import wx
import wx.html2
import numpy as np
import wx.lib.inspection

import pandas as pd

from utils.readLas import ReadLas
from utils.commons import show_message_dialog, add_html_to_browser_page

from plots.log_plot import PlotLog
from plots.correlation_plot import SelectCorrelationPlotField, PlotCorrelation
from plots.plot_3d import plot_3d, Plot3dDlg
from plots.overlay_plot import SetOverlayProperties, PlotOverlaySet
from plots.cross_plot import PlotCross, SetCrossPlotProperties

from ml import main
from sklearn.ensemble import RandomForestRegressor

from ui_main import ui
from ui_main.las.load_las.well_select_dialog import SelectWellDialog
from ui_main.tools.interpolate.petrophysics.prediction.prediction_dialog import PredictionDialog
from ui_main.tools.interpolate.petrophysics.validation.validation_dialog import ValidationDialog, ValidationPlot
from ui_main.tools.interpolate.facies.facies_interpolate import facies_csv_dlg
from ui_main.file.new_project import NewProjectDialog
from ui_main.file.open_project import open_project_dlg
from ui_main.initial_dialog import InitialDialog
from ui_main.file.save_project import save_project_to_file
from ui_main.plot_notebook import PlotNotebook

from analysis.vshale import gr_analysis

from sklearn.linear_model import LinearRegression, LogisticRegression, RandomizedLogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, BaggingRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from pykrige.rk import RegressionKriging

string_to_method = {
    'LinearRegression': LinearRegression,
    'LogisticRegression': LogisticRegression,
    'RandomizedLogisticRegression': RandomizedLogisticRegression,
    'DecisionTreeRegressor': DecisionTreeRegressor,
    'RandomForestRegressor': RandomForestRegressor,
    'AdaBoostRegressor': AdaBoostRegressor,
    'BaggingRegressor': BaggingRegressor,
    'GradientBoostingRegressor': GradientBoostingRegressor,
    'SVR': SVR,
    'RegressionKriging': RegressionKriging
}




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

    def set_statusbar_text(self, text):
        self.statusbar.SetStatusText(text)

    def load_las_dlg(self, event):
        openFileDialog = wx.FileDialog(self, "Open", "", "",
                                       "LAS files (*.las)|*.las",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        path = openFileDialog.GetPath()
        file_name = ntpath.basename(path)[:-4]  # [:-4] remove .las extension from filename
        dlg = SelectWellDialog(self, list(self.wells.keys()), file_name)
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val != wx.ID_OK:
            return
        well_name = dlg.get_well_name()
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

    def plot_log(self, event):
        selected = self.get_selected_df_list()
        num_selected = len(selected)
        if num_selected == 1:
            df = selected[0]
            plt_log_obj = PlotLog(df)
            html_string = plt_log_obj.get_html_string()
            add_html_to_browser_page(self.panel_right, self.plotter, html_string, "Log Plot")
        else:
            show_message_dialog(self, 'Only one well should be selected for Log Plot',
                                'Error', )

    def correlation_plot(self, event):

        # TODO assumption here: only one LAS selected per well

        df_arr = self.get_selected_df_list()
        well_names = list(self.selected_dict.keys())
        if (len(df_arr) < 2):
            show_message_dialog(self,
                                'At least two wells needs to be selected for Correlation Plot',
                                'Error',)
        else:
            common_fields = self._get_common_fields()
            dlg = SelectCorrelationPlotField(self, common_fields)
            dlg.SetSize(250, -1)
            dlg.CenterOnScreen()
            val = dlg.ShowModal()
            if val != wx.ID_OK:
                return
            choice_field = dlg.get_selection()
            plot_obj = PlotCorrelation(self.panel_right, self.plotter, df_arr, choice_field, well_names)
            html_string = plot_obj.get_html_string()
            add_html_to_browser_page(self.panel_right, self.plotter, html_string, "Correlation plot")

    def overlay_plot(self, event):
        df_arr = self.get_selected_df_list()
        num_selected = len(df_arr)
        if num_selected == 1:
            df = df_arr[0]
            choices = df.columns[:-2]
            dlg = SetOverlayProperties(self, choices)
            dlg.CenterOnScreen()
            val = dlg.ShowModal()
            if val != wx.ID_OK:
                return
            props_to_relate = dlg.get_selection()
            plot_obj = PlotOverlaySet(self.panel_right, self.plotter, df, props_to_relate)
            html_string = plot_obj.get_html_string()
            add_html_to_browser_page(self.panel_right, self.plotter, html_string, "Overlay plot")
        else:
            show_message_dialog(self, 'Only one well should be selected for Overlay Plot',
                                'Error', )

    def cross_plot(self, event):
        df_arr = self.get_selected_df_list()
        num_selected = len(df_arr)
        if num_selected == 1:
            df = df_arr[0]
            choices = df.columns[:-2]
            dlg = SetCrossPlotProperties(self, choices)
            dlg.CenterOnScreen()
            val = dlg.ShowModal()
            if val != wx.ID_OK:
                return
            props_to_relate = dlg.get_selection()
            plot_cross = PlotCross(df, props_to_relate)
            html_string = plot_cross.get_html_string()
            add_html_to_browser_page(self.panel_right, self.plotter, html_string, "Cross Plot")
        else:
            show_message_dialog(self, 'Only one well should be selected for Overlay Plot', 'Error')

    def on_gr_vshale(self, event):
        df_arr = self.get_selected_df_list()
        num_selected = len(df_arr)
        if num_selected == 1:
            dlg = gr_analysis.GrMinMaxSelect(self, df_arr[0])
            modal_val = dlg.ShowModal()
            if modal_val != wx.ID_OK:
                return
            gr_min_max = dlg.get_min_max()
            plot_obj = gr_analysis.GrAnalysis(df_arr[0], gr_min_max)
            html_string = plot_obj.get_html_string()
            add_html_to_browser_page(self.panel_right, self.plotter, html_string, "GR Plot")
        else:
            show_message_dialog(self, 'Only one well should be selected for GR Plot',
                                'Error', )

    def _get_common_fields(self):
        col_arr = []
        selected_list = self.get_selected_df_list()
        for selected in selected_list:
            col_arr.append(selected.columns)
        common_fields = col_arr[0]
        for col in col_arr:
            common_fields = common_fields.intersection(col)
        common_list = common_fields.tolist()
        return common_list

    def get_selected_df_list(self, with_lat_long=False):
        self.selected_df_list = []
        self.selected_dict = {}
        for well_name in self.well_to_tree:
            tree = self.well_to_tree[well_name]
            children = tree.GetChildren()
            for index, child in enumerate(children):
                if child.IsChecked():
                    if with_lat_long:
                        to_append = self.wells[well_name][index].df
                    else:
                        to_append = self.wells[well_name][index].df.drop(columns =['lat', 'long'])
                    self.selected_df_list.append(to_append)
                    if well_name in self.selected_dict:
                        if index not in self.selected_dict[well_name]:
                            self.selected_dict[well_name].append(index)
                    else:
                        self.selected_dict[well_name] = [index]
        return self.selected_df_list

    def on_prediction(self, event):
        common_fields = self._get_common_fields()
        dlg = PredictionDialog(self, common_fields, list(string_to_method.keys()))
        modal_val = dlg.ShowModal()
        if modal_val != wx.ID_OK:
            return
        selected_method = dlg.get_selected_method()
        num_wells = int(dlg.get_num_wells())
        selected_df_list = self.get_selected_df_list(with_lat_long=True)
        num_selected = len(selected_df_list)
        if num_selected >= 3:
            try:
                self.set_statusbar_text('Prediction started')
                self.predicted_df = main.prediction(selected_df_list, num_wells, string_to_method[selected_method])
                self.set_statusbar_text('Prediction completed')
                self.string_prediction = selected_method + " " + str(num_selected) + "wells"
            except Exception as e:
                show_message_dialog(self, 'Prediction failed with error: ' + repr(e),
                                    'Error')
                self.set_statusbar_text('Prediction failed')
        else:
            show_message_dialog(self, 'At least three wells should be selected for prediction',
                                'Error')

    def on_validation(self, event):
        common_fields = self._get_common_fields()
        dlg = ValidationDialog(self, common_fields, list(string_to_method.keys()))
        modal_val = dlg.ShowModal()
        if modal_val != wx.ID_OK:
            return
        selected_method = dlg.get_selected_method()
        selected_scoring = dlg.get_selected_scoring()
        selected_df_list = self.get_selected_df_list(with_lat_long=True)
        self.set_statusbar_text("Validation started")
        scores_df = main.validation(selected_df_list, string_to_method[selected_method], selected_scoring)
        self.set_statusbar_text("Validation Finished")
        plt = ValidationPlot(scores_df, 'Title')
        html_string = plt.get_html_string()
        add_html_to_browser_page(
            self.panel_right,
            self.plotter, html_string,
            "Scoring " + selected_method + " " + selected_scoring
        )
        self.set_statusbar_text("Plot Successful")

    def on_3d_plot(self, event):
        props = self._get_common_fields()
        dlg = Plot3dDlg(self, props)
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            prop_to_plot = dlg.get_selection()
            try:
                self.set_statusbar_text("3d Plotting started")
                plot_3d(
                    self.plotter,
                    self.predicted_df,
                    prop_to_plot,
                    "3d plot "+ self.string_prediction
                )
                self.set_statusbar_text("3d Plotting started")
            except AttributeError:
                self.set_statusbar_text("3d Plotting failed")
                show_message_dialog(
                    self,
                    'Please run prediction first. Currently, '
                    '3d plot runs only in conjecture of prediction',
                    'Error')


    def on_interpolate_facies(self, event):
        df_arr = self.get_selected_df_list()
        num_selected = len(df_arr)
        if num_selected == 1:
            facies_path = facies_csv_dlg(self)
            facies_df = pd.read_csv(facies_path)
            #some_func
        else:
            show_message_dialog(self, 'Only one well should be selected for Facies plot',
                                'Error', )

    def new_project(self, event):
        dlg = NewProjectDialog(self)
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val != wx.ID_OK:
            return
        # name = os.path.basename(path)
        # self.project_name = name
        # self.project_path = path

    def open_project(self, event):
        open_project_dlg(self)
        # TODO it does nothing right now

    def save_project(self, event):
        wells_modified = {k: list(map(lambda x: x.read_path, v)) for k, v in self.wells.items()}
        save_project_to_file(wells_modified, self.project_path)


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
