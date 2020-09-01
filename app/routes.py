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
    students_query = Student.query
    for category in filters:
        # TODO: do this more cleanly
        #students_query.filter_by(**{fil: Student.
        if category == 'college':
            students_query.filter(Student.year.in_(filters[category]))
        elif category == 'year':
            students_query.filter(Student.year.in_(filters[category]))
    students = students_query.all()
    return jsonify([student.email for student in students])

@app.route('/scraper', methods=['GET', 'POST'])
def scraper():
    if request.method == 'GET':
        return render_template('scraper.html')
    payload = request.get_json()

