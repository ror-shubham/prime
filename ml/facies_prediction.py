import numpy as np
import warnings
from sklearn import preprocessing
from sklearn.ensemble import GradientBoostingClassifier

warnings.simplefilter(action='ignore', category=FutureWarning)


def facies_prediction(feature_df, label_df, test_df, algorithm, features_to_train=['GR', 'NEUT']):
    # TODO 'priority 1' features_to_train is currently hardcoded.
    algorithm = GradientBoostingClassifier
    abhi = np.array(feature_df['DEPTH'])
    pra = np.array(label_df['DEPTH'])
    idx = []
    for i in range(len(pra)):
        idx.append((np.abs(pra[i] - abhi)).argmin())

    if idx[0] != 0:
        feature_df = feature_df[idx[0]:][:]
    feature_df['facies'] = np.nan
    label_df['facies'].unique()
    li = []
    for i in range(len(idx) - 1):
        initial = idx[i]
        final = idx[i + 1]
        k = label_df.loc[i]['facies']
        for j in range(initial, final):
            li.append(k)
    #     print(int(x.iloc[initial]['DEPTH']), int(x.iloc[final]['DEPTH'] ), k )
    if (len(li) != len(feature_df)):
        for i in range(len(li), len(feature_df)):
            li.append(k)
    feature_df['facies'] = li

    df = feature_df.replace(-999.25, np.nan)
    df = df.dropna(axis=0)
    df = df.reset_index(drop=True)

    train_y = df['facies'].values

    feature_vectors = df.drop(['DEPTH', 'facies', 'lat', 'long'], axis=1)
    #     feature_vectors = df.drop(['DEPTH','facies',], axis=1)
    cols = feature_vectors.columns
    #     print(cols)
    #     if len(features_to_train)!=0:
    cols = np.intersect1d(cols, features_to_train)

    #     if len(cols==0):
    #         print('No common columns between selected and present in dataframe')

    feature_vectors = feature_vectors[features_to_train]

    scaler = preprocessing.StandardScaler().fit(feature_vectors)
    train_x = scaler.transform(feature_vectors)

    clf = algorithm()

    print(train_y)
    clf.fit(train_x, train_y)

    test = test_df
    test = test[features_to_train]
    test = test.replace(-999.25, np.nan)
    test = test.dropna(axis=0)
    depth = test_df['DEPTH']
    lat = test_df['lat']
    long = test_df['long']
    depth = depth.reset_index(drop=True)
    test = test[cols]
    test = test.reset_index(drop=True)
    test_matrix = scaler.transform(test)
    label_df = clf.predict(test_matrix)
    test['facies'] = label_df
    test['DEPTH'] = list(depth)
    test['lat'] = lat
    test['long'] = long
    return test