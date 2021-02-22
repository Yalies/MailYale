from flask import render_template, request, jsonify, g
from flask_cas import login_required
from app import app, db, cas
from app.models import User

import datetime
import time
import yalies

yalies_api = yalies.API(os.environ['YALIES_API_KEY'])

@app.before_request
def store_user():
    if request.method != 'OPTIONS':
        if cas.username:
            g.user = User.query.get(cas.username)
            timestamp = int(time.time())
            if not g.user:
                g.user = User(username=cas.username,
                              registered_on=timestamp)
                db.session.add(g.user)
            g.user.last_seen = timestamp
            db.session.commit()
            print('NetID: ' + cas.username)


@app.route('/')
def index():
    if not cas.username:
        return render_template('splash.html')
    filters = yalies_api.filters()
    return render_template('index.html', colleges=colleges,
                           years=years, leave=leave, majors=majors, building_codes=building_codes,
                           entryways=entryways, floors=floors, suites=suites, rooms=rooms, states=states)


@app.route('/query', methods=['POST'])
@login_required
def query():
    filters = request.get_json()
    students_query = Student.query
    for category in filters:
        if category not in ('college', 'year', 'major', 'building_code',
                            'entryway', 'floor', 'suite', 'room', 'state', 'leave'):
            abort(403)
        students_query = students_query.filter(getattr(Student, category).in_(filters[category]))
    students = students_query.all()
    return jsonify([student.email for student in students if student.email])
