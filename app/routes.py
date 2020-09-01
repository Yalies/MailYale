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
    return render_template('index.html', colleges=colleges, years=years, majors=majors)

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
    students = students_query.all()
    return jsonify([student.email for student in students])

@app.route('/scraper', methods=['GET', 'POST'])
def scraper():
    if request.method == 'GET':
        return render_template('scraper.html')
    payload = request.get_json()
    tasks.scrape.apply_async(args=[payload['cookie']])
    return '', 200
