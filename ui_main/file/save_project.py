import pickle

import wx
import wx.xrc


def save_project_to_file(wells, project_path):
    with open(project_path, 'wb') as f:
        pickle.dump(wells, f, pickle.HIGHEST_PROTOCOL)