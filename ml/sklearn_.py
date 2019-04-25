from sklearn.linear_model import LinearRegression,LogisticRegression,RandomizedLogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, BaggingRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

class interpolation():

    def __init__(self, train_df):
        self.train_df = train_df


    def validation(self, algorithm = RandomForestRegressor,property_ = 'RHOB',scoring='r2',kwds ={},cv=3):
        # try:
        if (algorithm == 'pykrige'):
            algorithm = BaggingRegressor
        clf = algorithm(**kwds)
        scores = cross_val_score(clf, self.train_df[['DEPTH', 'lat', 'long']], self.train_df[property_], cv=cv,
                                 scoring=scoring)
        print("Scoring ("+ scoring+") : %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        # TODO return something more sensible
        return "Scoring ("+ scoring+") : %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
        # except:
        #     print(str(str(algorithm).split("'")[-2].split('.')[-1]) + ' is not valid for this kind of data, try something different algorithms')



    def prediciton(self,test_df,property_ = 'RHOB',algorithm=RandomForestRegressor,kwds={}):
        algorithm=RandomForestRegressor
        # try:
        if(algorithm=='pykrige'):
            algorithm = BaggingRegressor

        clf = algorithm(**kwds)
        clf.fit(self.train_df[['DEPTH', 'lat', 'long']], self.train_df[property_])
        print('train done')
        pred = clf.predict(test_df)
        print('prediction done')
        test_df[property_] = pred
        return test_df
        #except:
         #   print(str(str(algorithm).split("'")[-2].split('.')[-1]) + ' is not valid for this kind of data, try something different algorithms')







