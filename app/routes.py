from flask import render_template, request, jsonify
from flask_cas import login_required
from app import app, db, tasks
from app.models import Student
from sqlalchemy import distinct

import datetime


@app.route('/')
def index():
    colleges = [
        'Berkeley',
        'Branford',
        'Davenport',
        'Ezra Stiles',
        'Jonathan Edwards',
        'Benjamin Franklin',
        'Grace Hopper',
        'Morse',
        'Pauli Murray',
        'Pierson',
        'Saybrook',
        'Silliman',
        'Timothy Dwight',
        'Trumbull',
    ]
    building_codes = {
        '': 'Off Campus',
        'BM': 'Bingham Hall',
        'W': 'Welch Hall',
        'F': 'Farnam Hall',
        'D': 'Durfee Hall',
        'L': 'Lawrance Hall',
        'V': 'Vanderbilt Hall',
        'LW': 'Lanman-Wright Hall',
        'BK': 'Berkeley',
        'BR': 'Branford',
        'DC': 'Davenport',
        'ES': 'Ezra Stiles',
        'JE': 'Jonathan Edwards',
        'BF': 'Benjamin Franklin',
        'GH': 'Grace Hopper',
        'MC': 'Morse',
        'MY': 'Pauli Murray',
        'PC': 'Pierson',
        'SY': 'Saybrook',
        'SM': 'Silliman',
        'TD': 'Timothy Dwight',
        'TC': 'Trumbull',
    }
    current_year = datetime.date.today().year
    years = list(range(current_year, current_year + 5))
    years.append('')
    majors = [
        '',
        'Undeclared',
        'Visiting International Program',
        'African American Studies',
        'African Studies',
        'American Studies',
        'American Studies (Int.)',
        'Anthropology',
        'Applied Mathematics',
        'Applied Physics',
        'Archaeological Studies',
        'Architecture',
        'Art',
        'Astronomy',
        'Astrophysics',
        'Biomedical Engineering',
        'Chemical Engineering',
        'Chemistry',
        'Chemistry (Int.)',
        'Classical Civilization',
        'Classics',
        'Classics (Int.)',
        'Cognitive Science',
        'Comparative Literature',
        'Computer Science',
        'Computer Science & Econ',
        'Computer Science & Mathematics',
        'Computer Science & Psychology',
        'Computing and the Arts',
        'Earth and Planetary Sciences',
        'East Asian Languages & Lits',
        'East Asian Studies',
        'Ecology & Evolutionary Biology',
        'Economics',
        'Economics & Mathematics',
        'Elec.Engineering/Computer Sci',
        'Electrical Engineering',
        'Engineering Sci-Environmental',
        'Engineering Science-Chemical',
        'Engineering Science-Electrical',
        'Engineering Science-Mechanical',
        'English',
        'Environmental Engineering',
        'Environmental Studies',
        'Ethics,Politics & Economics',
        'Ethnicity, Race & Migration',
        'Film and Media Studies',
        'Film and Media Studies (Int.)',
        'French',
        'German Studies',
        'Global Affairs',
        'Greek, Ancient & Modern',
        'History',
        'History Science, Medicine & PH',
        'History of Art',
        'Humanities',
        'Italian',
        'Judaic Studies',
        'Latin American Studies',
        'Linguistics',
        'Lit. and Comparative Cultures',
        'Mathematics',
        'Mathematics & Philosophy',
        'Mathematics & Physics',
        'Mathematics (Int.)',
        'Mechanical Engineering',
        'Modern Middle Eastern Studies',
        'Molecular Biophysics & Biochem',
        'Molecular,Cellular,Dev Biology',
        'Molecular,Cellular,DevBio(Int)',
        'Music',
        'Music (Int.)',
        'Near Eastern Languages & Civs',
        'Neuroscience',
        'Philosophy',
        'Physics',
        'Physics & Geosciences',
        'Physics & Philosophy',
        'Physics (Int.)',
        'Political Science',
        'Political Science (Int.)',
        'Psychology',
        'Religious Studies',
        'Russian',
        'Russian & E European Studies',
        'Sociology',
        'Sociology (Int.)',
        'Spanish',
        'Special Divisional Major',
        'Statistics and Data Science',
        'Theater & Performance Studies',
        'Urban Studies',
        'Women\'sGender&SexualityStudies',
    ]
    entryways = db.session.query(distinct(Student.entryway)).order_by(Student.entryway)
    floors = db.session.query(distinct(Student.floor)).order_by(Student.floor)
    suites = db.session.query(distinct(Student.suite)).order_by(Student.suite)
    rooms = db.session.query(distinct(Student.room)).order_by(Student.room)
    # SQLAlchemy returns lists of tuples, so we gotta convert to a list of items.
    # TODO: is there a SQL-based way to do this?
    entryways = untuple(entryways)
    floors = untuple(floors)
    suites = untuple(suites)
    rooms = untuple(rooms)
    return render_template('index.html', colleges=colleges,
                           years=years, majors=majors, building_codes=building_codes,
                           entryways=entryways, floors=floors, suites=suites, rooms=rooms)


@app.route('/query', methods=['POST'])
def query():
    filters = request.get_json()
    students_query = Student.query
    for category in filters:
        # TODO: do this more cleanly
        #students_query.filter_by(**{fil: Student.
        if category == 'college':
            students_query = students_query.filter(Student.college.in_(filters[category]))
        elif category == 'year':
            students_query = students_query.filter(Student.year.in_(filters[category]))
        elif category == 'major':
            students_query = students_query.filter(Student.major.in_(filters[category]))
    students = students_query.all()
    return jsonify([student.email for student in students if student.email])


@app.route('/scraper', methods=['GET', 'POST'])
def scraper():
    if request.method == 'GET':
        return render_template('scraper.html')
    payload = request.get_json()
    tasks.scrape.apply_async(args=[payload['cookie']])
    return '', 200


def untuple(tuples):
    return [t[0] for t in tuples]
