from app import app, db, celery
from app.models import Student

import os
import re
from bs4 import BeautifulSoup
import usaddress


with open('app/res/majors.txt') as f:
    MAJORS = f.read().splitlines()
RE_ROOM = re.compile(r'^([A-Z]+)-([A-Z]+)(\d+)(\d)([A-Z]+)?$')
RE_BIRTHDAY = re.compile(r'^[A-Z][a-z]{2} \d{1,2}$')


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


def get_tree(html):
    print('Building tree.')
    tree = BeautifulSoup(html, 'html.parser')
    print('Done building tree.')
    return tree


def clean_name(name):
    print('Parsing ' + name)
    forename, surname = name.strip().split(', ', 1)
    return forename, surname


def clean_year(year):
    year = year.lstrip('\'')
    if not year:
        return None
    return 2000 + int(year)


def guess_email(student):
    return (student.forename + '.' + student.surname).replace(' ', '').lower() + '@yale.edu'


def parse_address(address):
    # Remove duplicates
    address = list(dict.fromkeys(address))
    address = ', '.join(address)
    try:
        components = usaddress.parse(address)
        options = [
            component for component, label in components
            if label == 'StateName' and len(component) == 2 and component.isupper()
        ]
        if options:
            return options[0]
    except usaddress.RepeatedLabelError:
        pass


@celery.task
def scrape(cookie):
    html = get_html(cookie)
    tree = get_tree(html)
    containers = tree.find_all('div', {'class': 'student_container'})

    # Clear all students
    Student.query.delete()
    for container in containers:
        student = Student()

        student.surname, student.forename = clean_name(container.find('h5', {'class': 'yalehead'}).text)
        student.year = clean_year(container.find('div', {'class': 'student_year'}).text)
        student.pronoun = container.find('div', {'class': 'student_info_pronoun'}).text

        info = container.find_all('div', {'class': 'student_info'})

        student.college = info[0].text.replace(' College', '')
        try:
            student.email = info[1].find('a').text
        except AttributeError:
            student.email = guess_email(student)
        trivia = info[1].find_all(text=True, recursive=False)
        try:
            room = trivia.pop(0) if RE_ROOM.match(trivia[0]) else None
            if room:
                result = RE_ROOM.search(room)
                student.building_code, student.entryway, student.floor, student.suite, student.room = result.groups()
            student.birthday = trivia.pop() if RE_BIRTHDAY.match(trivia[-1]) else None
            student.major = trivia.pop() if trivia[-1] in MAJORS else None
            student.address = ', '.join(trivia)
            student.state = parse_address(trivia)
        except IndexError:
            pass

        db.session.add(student)

    db.session.commit()
    print('Done.')
