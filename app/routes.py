from flask import render_template
from app import app, tasks

import json


@app.route('/')
def index():
    return render_template('index.html')