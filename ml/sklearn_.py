from sklearn.ensemble import RandomForestRegressor, BaggingRegressor
from sklearn.model_selection import cross_val_score
import warnings
from pykrige.rk import RegressionKriging

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


class interpolation():

    def __init__(self, train_df):
        self.train_df = train_df

    def validation(self, algorithm=RandomForestRegressor, property_='RHOB', scoring='r2', kwds={}, cv=3):
        if algorithm == 'pykrige':
            algorithm = RegressionKriging
        clf = algorithm(**kwds)
        scores = cross_val_score(clf, self.train_df[['DEPTH', 'lat', 'long']], self.train_df[property_], cv=cv,
                                 scoring=scoring)
        print("Scoring (" + scoring + ") : %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        # TODO return scores
        return scores

    def prediction(self, test_df, property_='RHOB', algorithm=RandomForestRegressor, kwds={},
                   columns_to_train=['DEPTH', 'lat', 'long']):
        if algorithm == 'pykrige':
            algorithm = BaggingRegressor

        clf = algorithm(**kwds)
        clf.fit(self.train_df[columns_to_train], self.train_df[property_])
        pred = clf.predict(test_df[columns_to_train])
        test_df[property_] = pred
        return test_df
