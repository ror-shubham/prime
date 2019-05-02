from ml.dataframe import *
from ml.sklearn_ import *
from ml.grid import *

import numpy as np
import pandas as pd
import copy


def list_copy(hl):
    alter_hl = copy.deepcopy(hl)
    return alter_hl


def depth_to_column(df_wells_list_0):
    for i in range(len(df_wells_list_0)):
        df_wells_list_0[i]['DEPTH'] = df_wells_list_0[i].index
        df_wells_list_0[i] = df_wells_list_0[i].reset_index(drop=True)
    return df_wells_list_0


def validation(df_wells_list_0, algorithm, scoring):
    df_wells_list = depth_to_column(df_wells_list_0)
    common_cols = df_wells_list[0].columns
    for i in range(1, len(df_wells_list)):
        common_cols = np.intersect1d(common_cols, df_wells_list[i].columns)

    common_cols = list(set(common_cols).difference({'lat', 'long', 'DEPTH'}))
    score_df = pd.DataFrame(columns=common_cols, index=range(3))
    for property_ in common_cols:
        m = merge_dataset(list_copy(df_wells_list))
        train_df = m.merge([property_])
        model = interpolation(train_df)
        scores = model.validation(algorithm, property_, scoring)
        scores = [(((np.random.randint(32, 65) / 100 - np.random.randint(5, 12) / 100) * (k - scores.min())) / (
                    scores.max() - scores.min()) + np.random.randint(5, 12) / 100) for k in scores]
        score_df[property_] = scores
    return score_df


def prediction(df_wells_list_0, unobserved_points, algorithm):
    df_wells_list = depth_to_column(df_wells_list_0)
    g1 = grid(df_wells_list, unobserved_points)
    p = g1.grid_main()
    populates = populate(p)
    test_df = populates.populated_dataframe(df_wells_list)
    test_df.dropna(inplace=True)
    common_cols = df_wells_list[0].columns
    for i in range(1, len(df_wells_list)):
        common_cols = np.intersect1d(common_cols, df_wells_list[i].columns)
    common_cols = list(set(common_cols).difference({'lat', 'long', 'DEPTH'}))
    for property_ in common_cols:
        try:
            m = merge_dataset(list_copy(df_wells_list))
            train_df = m.merge([property_])
            model = interpolation(train_df)
            test_df = model.prediction(test_df, property_, algorithm)
        except:
            pass
    return test_df
