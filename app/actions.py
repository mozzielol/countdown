from app import app
from flask import render_template
from app.xmlparser import xml_to_dict, delete_element, add_new, daily_update
from flask import request
from _datetime import datetime


@app.route('/achieve_action')
def achieve_action():
    ddl_name = request.args.get('ddl_name', None)
    deadlines = xml_to_dict('app/xmls/countdown.xml')
    data = None
    for ddl in deadlines:
        if ddl['name'] == ddl_name:
            data = ddl
    add_new('app/xmls/milestones.xml', data)
    delete_element('countdown.xml', ddl_name)
    deadlines = xml_to_dict('app/xmls/countdown.xml')
    return render_template('countdown.html', deadlines=deadlines)


@app.route('/delete_action')
def delete_action():
    ddl_name = request.args.get('ddl_name', None)
    delete_element('countdown.xml', ddl_name)
    deadlines = xml_to_dict('app/xmls/countdown.xml')
    return render_template('countdown.html', deadlines=deadlines)


@app.route('/add_task', methods= ['POST', 'GET'])
def add_task():
    if request.method == 'POST':
        data = request.form
        print(data['Date'])
        date = datetime.strptime(data['Date'], '%Y-%m-%d')
        ddl = {}
        ddl['year'] = date.year
        ddl['month'] = date.month
        ddl['day'] = date.day
        ddl['name'] = data['name']
        ddl['description'] = data['description']
        add_new('app/xmls/countdown.xml', ddl)

    return render_template('add.html')


@app.route('/add_daily_task', methods= ['POST', 'GET'])
def add_daily_task():
    if request.method == 'POST':
        data = request.form
        print(data['Date'])
        date = datetime.strptime(data['Date'], '%Y-%m-%d')
        ddl = {}
        ddl['year'] = date.year
        ddl['month'] = date.month
        ddl['day'] = date.day
        ddl['name'] = data['name']
        ddl['description'] = data['description']
        ddl['last'] = '0'
        add_new('app/xmls/dailywork.xml', ddl)
    deadlines = xml_to_dict('app/xmls/dailywork.xml', reverse=True)
    return render_template('daily.html', deadlines=deadlines)


# @app.route('/delete_daily_action')
# def delete_daily_action():
#     ddl_name = request.args.get('ddl_name', None)
#     delete_element('dailywork.xml', ddl_name)
#     deadlines = xml_to_dict('app/xmls/dailywork.xml')
#     return render_template('daily.html', deadlines=deadlines)


@app.route('/achieve_daily_action')
def achieve_daily_action():
    ddl_name = request.args.get('ddl_name', None)
    daily_update('dailywork.xml', ddl_name)
    deadlines = xml_to_dict('app/xmls/dailywork.xml', reverse=True)
    return render_template('daily.html', deadlines=deadlines)


@app.route('/undo_daily_action')
def undo_daily_action():
    ddl_name = request.args.get('ddl_name', None)
    daily_update('dailywork.xml', ddl_name, undo=True)
    deadlines = xml_to_dict('app/xmls/dailywork.xml', reverse=True)
    return render_template('daily.html', deadlines=deadlines)


@app.route('/milestone_daily_action')
def milestone_daily_action():
    ddl_name = request.args.get('ddl_name', None)
    deadlines = xml_to_dict('app/xmls/dailywork.xml', reverse=True)
    data = None
    for ddl in deadlines:
        if ddl['name'] == ddl_name:
            data = ddl
    add_new('app/xmls/daily_milestones.xml', data)
    delete_element('dailywork.xml', ddl_name)
    deadlines = xml_to_dict('app/xmls/dailywork.xml', reverse=True)
    return render_template('daily.html', deadlines=deadlines)