from ml.dataframe import *
from ml.sklearn_ import *
from ml.grid import *


def depth_to_column (df_wells_list_0):
    for i in range(len(df_wells_list_0)):
        df_wells_list_0[i]['DEPTH'] = df_wells_list_0[i].index
        df_wells_list_0[i] = df_wells_list_0[i].reset_index(drop=True)
    return df_wells_list_0


def validation(df_wells_list_0, property_, algorithm, scoring):
    df_wells_list = depth_to_column(df_wells_list_0)
    m = merge_dataset(df_wells_list)
    train_df = m.merge([property_])
    model = interpolation(train_df)
    scores = model.validation(algorithm, property_, scoring)
    return scores


def prediction(df_wells_list_0,property_,unobserved_points,algorithm):
    df_wells_list = depth_to_column(df_wells_list_0)
    g1 = grid(df_wells_list, unobserved_points)
    p = g1.grid_main()
    populates = populate(p)
    test_df = populates.populated_dataframe(df_wells_list)
    test_df.dropna(inplace=True)
    m = merge_dataset(df_wells_list)
    train_df = m.merge([property_])
    model = interpolation(train_df)
    test_df = model.prediciton(test_df,property_,algorithm)
    return test_df




