from app import app, db, celery
from app.models import Student

import os
import pickle
import re
from bs4 import BeautifulSoup
import usaddress


with open('app/res/majors.txt') as f:
    majors = f.read().splitlines()


def get_html(cookie):
    filename = 'page.html'
    if not os.path.exists(filename):
        print('Page not cached, fetching.')
        r = requests.get('https://students.yale.edu/facebook/PhotoPageNew',
                         params={
                             'currentIndex': -1,
                             'numberToGet': -1,
                         },
                         headers={
                             'Cookie': cookie,
                         })
        html = r.text
        with open(filename, 'w') as f:
            f.write(html)
        print('Done fetching page.')
    else:
        print('Using cached page.')
        with open(filename, 'r') as f:
            html = f.read()
    return html


def get_tree(cookie):
    filename = 'tree.pickle'
    if not os.path.exists(filename):
        print('Tree not cached, fetching.')
        html = get_html(cookie)
        print('Building tree.')
        tree = BeautifulSoup(html, 'html.parser')
        with open(filename, 'wb') as f:
            pickle.dump(tree, f)
        print('Done building tree.')
    else:
        with open(filename, 'rb') as f:
            tree = pickle.load(f)
    return tree


def clean_year(year):
    year = year.lstrip('\'')
    if not year:
        return None
    int(.replace('\'', '20'))
        if year == 20:
            year = None


def parse_address(address):
    # Remove duplicates
    address = list(dict.from_keys(address))
    address = ', '.join(address)
    try:
        components, _ = usaddress.tag(address)
        return components.get('StateName')
    except usaddress.RepeatedLabelError:
        return None


@celery.task
def scrape(cookie):
    tree = get_tree()
    containers = tree.find_all('div', {'class': 'student_container'})

    RE_ROOM = re.compile(r'^([A-Z]+)-([A-Z]+)(\d+)(\d)([A-Z]+)?$')
    RE_BIRTHDAY = re.compile(r'^[A-Z][a-z]{2} \d{1,2}$')
    # Clear all students
    Student.query.delete()
    for container in containers:
        student = Student()

        info = container.find_all('div', {'class': 'student_info'})
        name = container.find('h5', {'class': 'yalehead'}).text.strip()
        print('Parsing ' + name)
        student.surname, student.forename = name.split(', ', 1)
        student.forename = student.forename.strip()
        student.surname = student.surname.strip()

        student.year = clean_year(container.find('div', {'class': 'student_year'}).text)
        student.college = info[0].text.replace(' College', '')
        student.pronoun = container.find('div', {'class': 'student_info_pronoun'}).text
        try:
            student.email = info[1].find('a').text
        except AttributeError:
            student.email = (forename + '.' + surname).replace(' ', '').lower() + '@yale.edu'
        trivia = info[1].find_all(text=True, recursive=False)
        try:
            room = trivia.pop(0) if RE_ROOM.match(trivia[0]) else None
            if room:
                result = RE_ROOM.search(room)
                student.building_code, student.entryway, student.floor, student.suite, student.room = result.groups()
            student.birthday = trivia.pop() if RE_BIRTHDAY.match(trivia[-1]) else None
            student.major = trivia.pop() if trivia[-1] in majors else None
            student.address = ', '.join(trivia)
            student.state = parse_address(trivia)
        except IndexError:
            pass

        db.session.add(student)

    db.session.commit()
    print('Done.')
