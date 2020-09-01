from flask import render_template
from app import app, tasks

import json


@app.route('/')
def index():
    colleges = [
        'Berkeley College',
        'Branford College',
        'Davenport College',
        'Ezra Stiles College',
        'Jonathan Edwards College',
        'Benjamin Franklin College',
        'Grace Hopper College',
        'Morse College',
        'Pauli Murray College',
        'Pierson College',
        'Saybrook College',
        'Silliman College',
        'Timothy Dwight College',
        'Trumbull College',
    ]
    return render_template('index.html', colleges=colleges)

@app.route('/scraper')
def scraper():
    return render_template('scraper.html')
