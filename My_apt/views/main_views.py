from flask import Blueprint, request, render_template, redirect, url_for
from datetime import datetime
from My_apt.ml_model import AptSales_Model
from sklearn.ensemble import RandomForestRegressor

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main():
    month = str(datetime.today().month).zfill(2)
    day = str(datetime.today().day).zfill(2)
    year = datetime.today().year
    return render_template('main.html', month=month, day=day, year=year), 200

@main_bp.route('/', methods=['POST', 'GET'])
def get_input():
    if request.method == 'POST':
        apt_nm = request.form["apt"]
        apt_fl = request.form["floor"]
        apt_use = request.form["space"]
        return redirect(url_for("main.result", usr_info=[apt_nm, apt_fl, apt_use]))
    else:
        return render_template('main.html'), 200

@main_bp.route('/<usr_info>')
def result(usr_info):
    month = str(datetime.today().month).zfill(2)
    day = str(datetime.today().day).zfill(2)
    year = datetime.today().year
    usr_info = eval(usr_info)
    model = AptSales_Model()
    pred = model.predict_sales(RandomForestRegressor(), usr_info[0], usr_info[1], usr_info[2])
    return render_template('result.html', 
                            month=month, day=day, year=year, pred=int(pred[0]),
                            apt_nm=usr_info[0], apt_fl=usr_info[1], apt_use=usr_info[2]), 200