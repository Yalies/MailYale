from flask import render_template, request, jsonify
from app import app, tasks
from app.models import Student

import datetime


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
    current_year = datetime.date.today().year
    years = list(range(current_year, current_year + 5))
    return render_template('index.html', colleges=colleges, years=years)

@app.route('/query', methods=['POST'])
def query():
    filters = request.get_json()

    return jsonify(['erik.boesen@yale.edu'])

@app.route('/scraper')
def scraper():
    return render_template('scraper.html')
