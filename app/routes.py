from flask import render_template, request, jsonify, g
from flask_cas import login_required
from app import app, db, cas
from app.models import User

import datetime
import time
import yalies

yalies_api = yalies.API(app.config['YALIES_API_KEY'])

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
    options = yalies_api.filters()
    filters = {
        'Students': {
            'school': 'School',
            'year': 'Year',
        },
        'Graduate': {
            'curriculum': 'Curriculum',
        },
        'Undergraduate': {
            'college': 'College',
            'leave': 'Took Leave?',
            'major': 'Major',
            'eli_whitney': 'Eli Whitney?',
        },
        'Staff': {
            'organization': 'Organization',
            'unit': 'Organization Unit'
        },
    }
    return render_template('index.html', options=options, filters=filters)


@app.route('/query', methods=['POST'])
@login_required
def query():
    filters = request.get_json()
    people = yalies_api.people(filters=filters)
    return jsonify([person.email for person in people if person.email])
