import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly
import json
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from category_encoders import OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.compose import TransformedTargetRegressor
from sklearn.linear_model import LinearRegression, ElasticNetCV
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor, sklearn
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.pipeline import make_pipeline
import pickle
import datetime


class AptSales_Model:

    db_name = './My_apt/apt_sale.db'

    def __init__(self, db_name=db_name):
        self.conn, self.cur = self.sqlite_conn(db_name)
        self.df = self.read_table_to_df()


    ## connect to sqlite3
    def sqlite_conn(self, db_name):
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        return conn, cur

    ## read table from sql DB to convert to pandas dataframe
    def read_table_to_df(self):
        df = pd.read_sql('SELECT * FROM apt_sales;', self.conn, index_col='Id')
        return df

    def data_engineering(self):
        # print(self.db.dtypes)
        df_copy = self.df.copy()
        cols = df_copy.columns

        # remove columns named starting with "ROADNM_"
        new_cols_mask = cols.str.contains('ROADNM_', regex=False)
        new_cols = cols[~new_cols_mask]
        df_copy = df_copy[new_cols]

        # remove '-' from all values in "MANAGE_NO" column
        df_copy['MANAGE_NO'] = df_copy['MANAGE_NO'].str.replace('-', '')
        df_copy['LOTNO'] = df_copy['LOTNO'].apply(lambda x: str(x).replace('-', ''))

        # combine columns named starting with "LEGALDONG_" to create a new column
        # remove existing columns named starting with "LEGALDONG_"
        cols_mask_legal = new_cols.str.contains('LEGAL', regex=False)
        legal_cols = new_cols[cols_mask_legal][:-1]
        df_copy['new_LEGALDONG_CD'] = ''
        for legal_col in legal_cols:
            df_copy['new_LEGALDONG_CD'] += df_copy[legal_col]
        df_copy['new_LEGALDONG_CD'] = df_copy['new_LEGALDONG_CD'].astype('int')
        df_copy = df_copy.drop(legal_cols, axis=1)

        # create datetime column
        df_copy['DATETIME'] = df_copy['YEAR']+'-'+df_copy['MONTH'].str.zfill(2)+'-'+df_copy['DATE'].str.zfill(2)
        wrong_dates = ['04-31', '11-31', '02-31', '09-31', '06-31', '09-31', '02-31']
        right_dates = ['04-30', '11-30', '02-28', '09-30', '06-30', '09-30', '02-28']
        for i in range(len(wrong_dates)):
            df_copy['DATETIME'] = df_copy['DATETIME'].str.replace(wrong_dates[i], right_dates[i])
        df_copy['DATETIME'] = pd.to_datetime(df_copy['DATETIME'])
        df_copy['BUILD_YY'] = pd.to_datetime(df_copy['BUILD_YY']).dt.year
        df_copy['YEAR'] = df_copy['YEAR'].astype('int')
        df_copy['MONTH'] = df_copy['MONTH'].astype('int')
        df_copy.drop(['DATE'], axis=1,inplace=True)

        df_copy['SALES'] = df_copy['SALES'] * 10000

        ### save new df into sql table
        df_copy.to_sql('new_apt_sales', self.conn, if_exists='replace', index=False)
        # df_copy.to_csv('new_apt_sales.csv')
        self.conn.commit()

        return df_copy
        

    ## draw heatmap for correlations of data
    def plot_corr_heatmap(self):
        df = self.data_engineering().sort_values('DATETIME').reset_index(drop=True)
        target = 'SALES'
        plt.figure(figsize=(12, 10))    
        sns.heatmap(df.corr())
        plt.show()

    def plot_target_hist(self, log_transform=False):
        df = self.data_engineering().sort_values('DATETIME').reset_index(drop=True)
        target = 'SALES'
        target_df = df[target]
        if log_transform:
            target_df = np.log(df[target])
        plt.figure(figsize=(10, 8)) 
        sns.histplot(target_df)
        plt.show()

    ## split train and test data for 80:20 by Datetime
    def split_data(self):
        df = self.data_engineering().sort_values('DATETIME').reset_index(drop=True)
        split_index = int(len(df) * 0.8)
        target = 'SALES'

        train_df =  df[:split_index]
        test_df = df[split_index:]

        X_train = train_df.drop([target, 'DATETIME'], axis=1)
        y_train = train_df[target]
        X_test = test_df.drop([target, 'DATETIME'], axis=1)
        y_test = test_df[target]

        return X_train, X_test, y_train, y_test, train_df, test_df

    ## build regression model   
    def model(self, model_name, use_all_data=False):

        X_train, X_test, y_train, y_test, train_df, test_df = self.split_data()
        pipeline = make_pipeline(
                OrdinalEncoder(),
                SimpleImputer(),
                StandardScaler(),
                TransformedTargetRegressor(
                    regressor=model_name, 
                    func=np.log, inverse_func=np.exp)
            )

        if use_all_data:
            return pipeline.fit(train_df, test_df)

        else:
            return pipeline.fit(X_train, y_train), X_test, y_test

    ## pickle the model
    def save_model(self, model_name, use_all_data=False):
        if use_all_data:
            pipeline = self.model(model_name, use_all_data=use_all_data)
        else:
            pipeline, _, _, = self.model(model_name, use_all_data=use_all_data)

        with open(f'./My_apt/models/{type(model_name).__name__}.pkl', 'wb') as pkl_file:
            pickle.dump(pipeline, pkl_file)
        return pkl_file

    def evaluate_model(self, model_name):
        pipeline, X_test, y_test = self.model(model_name)
        y_pred = pipeline.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = mean_squared_error(y_test, y_pred)**0.5
        r2 = r2_score(y_test, y_pred)

        with open(f'./My_apt/logs/{type(model_name).__name__}_{datetime.datetime.now()}.txt', 'w') as log_file:
            log_file.write(f"<BEGIN>\n<<<Model Description>>>\n")
            log_file.write("="*50+'\n')
            log_file.write(f"""{pipeline.named_steps['transformedtargetregressor'].regressor}\n""")
            log_file.write("-"*50+'\n')
            log_file.write(f"<<<{type(model_name).__name__} Evaluation Report>>>\n")
            log_file.write("="*50+'\n')
            log_file.write(f"MAE: {mae} KRW\n")
            log_file.write(f"RMSE: {rmse} KRW\n")
            log_file.write(f"R2_Score: {r2.round(2)}\n<END>")
        
        self.save_model(model_name)
    
    def predict_sales(self, model_name, apt_nm, apt_fl, apt_use):
        df = self.read_new_sql()
        cols = df.columns
        cols = cols.drop(['SALES', 'DATETIME'])
        ### 새롭게 입력받은 아파트 정보 가져오기
        data = self.make_new_data(apt_nm, apt_fl, apt_use)
        data_copy = data.copy()
        ### 기존 타겟 Sales 와 불필요한 DATETIME 제거하기
        data_copy.pop(1)
        data_copy.pop(-1)
        test_data = pd.DataFrame([data_copy], columns=cols)
        ### 저장된 모델 불러오기
        with open(f'./My_apt/models/{type(model_name).__name__}.pkl', 'rb') as pkl_file:
            model = pickle.load(pkl_file)
        y_pred = model.predict(test_data)

        ### 예측한 sales로 입력받은 데이터 row에 덮어쓰기
        data[1] = int(y_pred[0])
        new_data = tuple(data)
        ### 새로운 아파트 정보를 db에 저장하기
        self.write_new_sql(new_data)

        return y_pred
    
    def read_new_sql(self):
        df = pd.read_sql("SELECT * FROM new_apt_sales", self.conn)
        return df
    
    def get_data_with_aptnm(self, apt_nm):
        df = self.read_new_sql()
        gb_df = df.groupby("APT_NM")['SALES'].agg(['mean', 'min', 'max']).reset_index()
        mean_apt = gb_df[gb_df['APT_NM'] == apt_nm]
        # return int(mean_apt['mean']), int(mean_apt['min']), int(mean_apt['max'])
        new_df = mean_apt.T.reset_index()[1:]
        cols = new_df.columns.to_list()
        new_df = new_df.rename(columns={cols[0]:'method', cols[1]:'value'})
        return new_df
    
    def plot_apt(self, apt_nm):
        df = self.get_data_with_aptnm(apt_nm)
        fig = px.bar(df, x='method', y='value')
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    def write_new_sql(self, new_data):
        self.cur.execute("INSERT INTO new_apt_sales VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", new_data)
        self.conn.commit()

    def make_new_data(self, apt_nm, apt_fl, apt_use):
        ### 평수를 제곱미터로 변환
        apt_use = float(apt_use) * 3.3058
        ### 기본 아파트 정보 불러오기
        self.cur.execute(f"SELECT * FROM new_apt_sales WHERE APT_NM=='{apt_nm}' LIMIT 1;")
        data = list(self.cur.fetchone())
        ### 입력받은 아파트 정보로 갱신하기
        data[0] = int(datetime.datetime.now().year)
        data[-4] = int(datetime.datetime.now().month)
        data[4] = int(apt_fl)
        data[-3] = float(apt_use)
        data[-1] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        ### 새로운 아파트 정보를 반환하기
        return data
        


if __name__ == '__main__':
    model = AptSales_Model()
    # model.save_model(RandomForestRegressor(n_estimators=50, 
    #                                         criterion="squared_error", 
    #                                         max_depth=13, 
    #                                         min_samples_split=3, 
    #                                         min_samples_leaf=1, 
    #                                         max_leaf_nodes=None, n_jobs=-1, 
    #                                         random_state=1))
    # print(model.predict_sales(RandomForestRegressor(), "광복현대아파트", "15", "45"))
    # model.evaluate_model(RandomForestRegressor(n_estimators=50, 
    #                                         criterion="squared_error", 
    #                                         max_depth=13, 
    #                                         min_samples_split=3, 
    #                                         min_samples_leaf=1, 
    #                                         max_leaf_nodes=None, n_jobs=-1, 
    #                                         random_state=1))
    # model.evaluate_model(LGBMRegressor())
    print(model.plot_apt('광명한진타운'))