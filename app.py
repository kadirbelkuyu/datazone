
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from v4toclass import getMap
DEVELOPMENT_ENV  = True
from bar import get_barchar
import folium
import os
import random
import shutil
import time

app = Flask(__name__)

app_data = {
    "name":         "datazone",
    "description":  "",
    "author":       "datazone Team",
    "html_title":   "",
    "project_name": "",
    "keywords":     "datazone"
}

# from v2 import getMap

@app.route('/')
def index():

    return render_template('index.html', app_data=app_data)


@app.route('/about')
def about():
    return render_template('about.html', app_data=app_data)
    


@app.route('/camera')
def camera():
    return render_template('camera.html', app_data=app_data)


@app.route('/yedek')
def yedek():
    return render_template('yedek.html', app_data=app_data)

@app.route('/yedek2')
def yedek2():
    map = getMap.getmap()
    
    return map._repr_html_()
    



@app.route('/analiz')
def analiz():
    analiz = get_barchar().plotsbar()
    return render_template('analiz.html', app_data=app_data)

@app.route('/service')
def service():
    map = getMap.getmap()
    return map._repr_html_()

    #return render_template('service.html', app_data=app_data)


@app.route('/contact')
def contact():
    return render_template('contact.html', app_data=app_data)


if __name__ == '__main__':
    app.run(debug=DEVELOPMENT_ENV)
