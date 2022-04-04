# [ML] 집값 예측 인공지능 웹 API - 얼마요
https://my-apt.herokuapp.com/

## introduction
> This is Machine-learning Web API project for prediction of the value of apartments in Gwangmyung-si, Korea.
> 
> ![introduction](https://user-images.githubusercontent.com/61719257/149120484-8308a144-2f01-43fa-a9e2-d6e39db2e834.gif)

## Environment & Skills
> - MacOS
> - Whale / Chrome Browser
> - Python 3.8
>    - Library for WebScraping : requests, APScheduler
>    - Library for EDA & Data Preprocessing : Pandas, Numpy
>    - Library for Data Visualization : Matplotlib, Plotly, Folium
>    - Library for ML Models : sklearn, xgboost, lightgbm
> - Flask, HTML, CSS
> - Heroku
> - Metabase
> - ML MODELS
>     - Tree-based-Models : RandomForest Regressor, Xgboost Regressor, Lightgbm Regressor
>     - TransformedTargetRegressor : Log Transformed Linear Regression
> - Miri Canvas
> - OBS

## pipeline
![image](https://user-images.githubusercontent.com/61719257/149119826-169cded8-df6b-4c08-ac3b-c5372c0fd07c.png)

## Data
> 광명시 공공 데이터 open api
![openapi](https://user-images.githubusercontent.com/61719257/149121212-cd8dcc58-427c-4843-b382-316ce44f0bce.gif)
![mongodb](https://user-images.githubusercontent.com/61719257/149121228-f84a3828-c7e5-4cdb-881b-61961c768994.gif)

## Evaluation
|MODELS   |MAE    |RMSE   |R2_SCORE   |
|---------|-------|-------|-----------|
|LinearRegression|174718437.51 KRW|238319972.99 KRW|0.08|
|ElasticNetCV|274784163.17 KRW|360266710.18 KRW|-1.1|
|RandomForestRegressor|63981882.48 KRW|113676925.82 KRW|0.9|
|XGB Regressor|149348580.28 KRW|180378806.28 KRW|0.47|
|LGBM Regressor|154223908.87 KRW|186687372.47 KRW|0.44|
