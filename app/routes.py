from app import app
from flask import render_template
from app.xmlparser import xml_to_dict


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


@app.route('/countdown')
def countdown():
    deadlines = xml_to_dict('app/xmls/countdown.xml')
    return render_template('countdown.html', deadlines=deadlines)


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/daily')
def daily():
    deadlines = xml_to_dict('app/xmls/dailywork.xml', reverse=True)
    return render_template('daily.html', deadlines=deadlines)


@app.route('/milestones')
def milestones():
    deadlines = xml_to_dict('app/xmls/milestones.xml')
    dailywork = xml_to_dict('app/xmls/daily_milestones.xml', reverse=True)
    return render_template('milestones.html', deadlines=deadlines, dailywork=dailywork)


