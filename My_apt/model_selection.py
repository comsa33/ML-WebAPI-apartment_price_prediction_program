from ml_model import AptSales_Model
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.compose import TransformedTargetRegressor
from sklearn.linear_model import LinearRegression, ElasticNetCV
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from category_encoders import OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer
import numpy as np


class GridSearch_Model(AptSales_Model):
    db_name = './My_apt/apt_sale.db'
    def __init__(self, db_name=db_name):
        super().__init__(db_name)

        
    
    def model(self, model_name, params):
        X_train, X_test, y_train, y_test = self.split_data()

        if type(model_name).__name__.lower() == 'xgbregressor' or 'lgbmregressor':
            pipeline = make_pipeline(
                            OrdinalEncoder(),
                            SimpleImputer(),
                            StandardScaler())
            X_train = pipeline.fit_transform(X_train)
            X_test = pipeline.transform(X_test)
            tt = TransformedTargetRegressor(
                                regressor=GridSearchCV(model_name, param_grid=params), 
                                func=np.log, inverse_func=np.exp)                
            tt.fit(X_train, y_train, 
                        eval_set=[(X_train, y_train), (X_test, y_test)], 
                        early_stopping_rounds=100)
            y_pred = tt.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            rmse = mean_squared_error(y_test, y_pred)**0.5
            r2 = r2_score(y_test, y_pred)
            print(mae, rmse, r2)
            return tt.regressor
            
        else:
            pipeline = make_pipeline(
                OrdinalEncoder(),
                SimpleImputer(),
                StandardScaler(),
                TransformedTargetRegressor(
                    regressor=GridSearchCV(model_name, param_grid=params), 
                    func=np.log, inverse_func=np.exp))
            pipeline.fit(X_train, y_train)
            y_pred = pipeline.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            rmse = mean_squared_error(y_test, y_pred)**0.5
            r2 = r2_score(y_test, y_pred)
            print(mae, rmse, r2)
            return pipeline.named_steps['transformedtargetregressor'].regressor

        
        
        
if __name__ == '__main__':
    model = GridSearch_Model()
    params = {
        "n_estimators":[50], 
        "criterion":["squared_error"], 
        "max_depth":[13], 
        "min_samples_split":[3], 
        "min_samples_leaf":[1], 
        "max_leaf_nodes":[None],
        "oob_score":[True], 
        "n_jobs":[-1], 
        "random_state":[1], 
        "ccp_alpha":[0.] 
        }
    print(model.model(RandomForestRegressor(), params))
    # params = {'nthread':[4], #when use hyperthread, xgboost may become slower
    #           'objective':['reg:linear'],
    #           'learning_rate': [.0001], #so called `eta` value
    #           'max_depth': [None],
    #         #   'min_child_weight': [1],
    #           'silent': [1],
    #           'subsample': [0.7],
    #           'colsample_bytree': [0.7],
    #           'n_estimators': [500]}
    # print(model.model(XGBRegressor(random_state=1, cv=2, n_jobs=-1, verbose=True), params).__dir__())
    