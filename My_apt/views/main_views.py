from flask import Blueprint, request, render_template, redirect, url_for, send_file
from datetime import datetime
from My_apt.ml_model import AptSales_Model
from sklearn.ensemble import RandomForestRegressor
import pickle
import folium
import json

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main():
    month = str(datetime.today().month).zfill(2)
    day = str(datetime.today().day).zfill(2)
    year = datetime.today().year
    return render_template('home.html', month=month, day=day, year=year), 200

@main_bp.route('/predict/', methods=['POST', 'GET'])
def get_input():
    if request.method == 'POST':
        apt_nm = request.form["apt"]
        apt_fl = request.form["floor"]
        apt_use = request.form["space"]
        return redirect(url_for("main.result", usr_info=[apt_nm, apt_fl, apt_use]))
    else:
        month = str(datetime.today().month).zfill(2)
        day = str(datetime.today().day).zfill(2)
        year = datetime.today().year
        return render_template('predict.html', month=month, day=day, year=year), 200

@main_bp.route('/predict/<usr_info>')
def result(usr_info):
    month = str(datetime.today().month).zfill(2)
    day = str(datetime.today().day).zfill(2)
    year = datetime.today().year
    usr_info = eval(usr_info)
    model = AptSales_Model()
    graphJSON = model.plot_apt(usr_info[0])
    pred = model.predict_sales(RandomForestRegressor(), usr_info[0], usr_info[1], usr_info[2])
    pred = format(int(pred[0]/10000), ',')
    return render_template('result.html', 
                            month=month, day=day, year=year, pred1=str(pred)[:-1], pred2=str(pred)[-1:], graphJSON=graphJSON,
                            apt_nm=usr_info[0], apt_fl=usr_info[1], apt_use=usr_info[2]), 200

@main_bp.route('/dashboard')        
def dashboard():
    return render_template('dashboard.html'), 200

@main_bp.route('/dashboard/numeric')        
def dashboard2():
    return render_template('dashboard2.html'), 200

@main_bp.route('/predict/')        
def prediction():
    month = str(datetime.today().month).zfill(2)
    day = str(datetime.today().day).zfill(2)
    year = datetime.today().year
    return render_template('predict.html', month=month, day=day, year=year), 200

@main_bp.route('/project/pipeline')        
def pipeline():
    return render_template('pipeline.html'), 200

@main_bp.route('/project/database')        
def database():
    return render_template('database.html'), 200

@main_bp.route('/project/mymodel')        
def model():
    return render_template('model.html'), 200

@main_bp.route('/project/presentation')        
def presentation():
    return render_template('presentation.html'), 200

@main_bp.route('/map/folium')
def map():
    model = AptSales_Model()
    map_data = model.create_map_data()

    m = folium.Map(
    location=[37.45, 126.83],
    zoom_start=13.2,
    tiles='Stamen Toner')

    geo_data = './My_apt/gwangmyungsi.geojson'

    with open(geo_data, mode='rt', encoding='utf-8') as f:
        geo = json.loads(f.read())
        f.close()

    highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}

    choropleth = folium.Choropleth(geo_data=geo_data, 
                    data = map_data,
                    columns=['LEGALDONG_NM', 'SALES'],
                    key_on='feature.properties.EMD_KOR_NM',
                    fill_color='YlGnBu',
                    fill_opacity=0.8,
                    highlight_function=highlight_function,
                    nan_fill_color="white",
                    highlight=True,
                    legend_name='지역별(동) 아파트 매매가'
                    ).add_to(m)

    tooltip=folium.features.GeoJsonTooltip(
            fields=['EMD_KOR_NM'],
            aliases=['법정동명: '],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"))

    folium.LayerControl().add_to(m)
    choropleth.geojson.add_child(tooltip)


    return m._repr_html_()