from app import app, db, celery
from app.models import Student

import os
import time
import re
from bs4 import BeautifulSoup
import usaddress


def get_html():
    filename = 'page.html'
    if not os.path.exists(filename):
        print('Page not cached, fetching...')

        r = requests.get('https://students.yale.edu/facebook/PhotoPageNew',
                         params={
                             'currentIndex': -1,
                             'numberToGet': -1,
                         },
                         headers={
                             'Cookie': cookie,
                         })
        page_text = r.text
        with open(filename, 'w') as f:
            f.write(page_text)
        print('done.')
    else:
        with open(filename, 'r') as f:
            print('Loading cached page... ', end='')
            page_text = f.read()
            print('done.')


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
    html = get_html()

    print('Building BeautifulSoup tree.')
    page = BeautifulSoup(page_text, 'html.parser')
    containers = page.find_all('div', {'class': 'student_container'})
    # Clear all students
    Student.query.delete()
    for container in containers:
        info = container.find_all('div', {'class': 'student_info'})
        name = container.find('h5', {'class': 'yalehead'}).text.strip()
        print('Parsing ' + name)
        surname, forename = name.split(', ', 1)
        surname = surname.strip()
        forename = forename.strip()
        college = info[0].text.replace(' College', '')
        try:
            email = info[1].find('a').text
        except AttributeError:
            email = ''
        trivia = info[1].find_all(text=True, recursive=False)
        RE_ROOM = re.compile(r'^([A-Z]+)-([A-Z]+)(\d+)(\d)([A-Z]+)?$')
        RE_BIRTHDAY = re.compile(r'^[A-Z][a-z]{2} \d{1,2}$')
        with open('app/res/majors.txt') as f:
            majors = f.read().splitlines()
        room = None
        birthday = None
        major = None
        address = None
        state = None
        try:
            room = trivia.pop(0) if RE_ROOM.match(trivia[0]) else None
            birthday = trivia.pop() if RE_BIRTHDAY.match(trivia[-1]) else None
            major = trivia.pop() if trivia[-1] in majors else None
            address = ', '.join(trivia)
            state = parse_address(trivia)
        except IndexError:
            pass

        # Split up room number
        if room:
            result = RE_ROOM.search(room)
            building_code, entryway, floor, suite, room = result.groups()
        else:
            building_code = None
            entryway = None
            floor = None
            suite = None
            room = None
        year = int(container.find('div', {'class': 'student_year'}).text.replace('\'', '20'))
        if year == 20:
            year = None

        student = Student(
            forename=forename,
            surname=surname,
            year=year,
            college=college,
            pronoun=container.find('div', {'class': 'student_info_pronoun'}).text,
            # Guess an email based on name if none provided
            email=email or (forename + '.' + surname).replace(' ', '').lower() + '@yale.edu',
            building_code=building_code,
            entryway=entryway,
            floor=int(floor) if floor else None,
            suite=int(suite) if floor else None,
            room=room,
            birthday=birthday,
            major=major,
            address=address,
            state=state,
        )
        db.session.add(student)

    db.session.commit()
    print('Done.')
