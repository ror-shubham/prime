from sklearn.linear_model import LinearRegression, LogisticRegression, RandomizedLogisticRegression, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, BaggingRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import cross_val_score
import warnings
from pykrige.rk import RegressionKriging

import pandas as pd

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


class interpolation():

    def __init__(self, train_df):
        self.train_df = train_df

    def validation(self, algorithm=RandomForestRegressor, property_='RHOB', scoring='r2', kwds={}, cv=3):
        if (algorithm == RegressionKriging):
            p = self.train_df[['DEPTH']]
            x = self.train_df[['lat', 'long']]
            target = self.train_df[[property_]]
            clf = Lasso(**kwds)
            scores = cross_val_score(clf, self.train_df[['DEPTH', 'lat', 'long']], self.train_df[property_], cv=cv,
                                     scoring=scoring)
            return scores

        else:

            if (algorithm == KNeighborsRegressor):
                clf = algorithm(n_neighbors=5, weights='distance')
            else:
                clf = algorithm(**kwds)
            scores = cross_val_score(clf, self.train_df[['DEPTH', 'lat', 'long']], self.train_df[property_], cv=cv,
                                 scoring=scoring)
            print("Scoring (" + scoring + ") : %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
            return scores

    def prediction(self, test_df, property_='RHOB', algorithm=RandomForestRegressor, kwds={},
                   columns_to_train=['DEPTH', 'lat', 'long']):

        if (algorithm == KNeighborsRegressor):
            clf = algorithm(n_neighbors=5, weights='distance')
        if (algorithm == RegressionKriging):
            p = self.train_df[['DEPTH']]
            x = self.train_df[['lat', 'long']]
            target = self.train_df[[property_]]
            clf = Lasso(**kwds)
        else:
            clf = algorithm(**kwds)
        clf.fit(self.train_df[columns_to_train], self.train_df[property_])
        pred = clf.predict(test_df[columns_to_train])
        test_df[property_] = pred
        return test_df
