from app import app, db, celery
from app.models import Student

import os
import time
import re
from bs4 import BeautifulSoup

@celery.task
def scrape(cookie):
    headers = {
        'Cookie': cookie,
    }

    filename = 'page.html'
    if not os.path.exists(filename):
        print('Page not cached, fetching...')
        params = {
            'currentIndex': -1,
            'numberToGet': -1,
        }

        r = requests.get('https://students.yale.edu/facebook/PhotoPageNew',
                         params=params,
                         headers=headers)
        page_text = r.text
        with open(filename, 'w') as f:
            f.write(page_text)
        print('done.')
    else:
        with open(filename, 'r') as f:
            print('Loading cached page... ', end='')
            page_text = f.read()
            print('done.')

    # Parsing page

    RE_BIRTHDAY = re.compile(r"^[A-Z][a-z]{2} \d{1,2}$")

    print('Building BeautifulSoup tree.')
    page = BeautifulSoup(page_text, "html.parser")
    containers = page.find_all("div", {"class": "student_container"})
    # Clear all students
    Student.query.delete()
    for container in containers:
        info = container.find_all("div", {"class": "student_info"})
        name = container.find("h5", {"class": "yalehead"}).text.strip()
        print("Parsing " + name)
        surname, forename = name.split(", ", 1)
        surname = surname.strip()
        forename = forename.strip()
        college = info[0].text
        try:
            email = info[1].find("a").text
        except AttributeError:
            email = ""
        trivia = info[1].find_all(text=True, recursive=False)
        RE_ROOM = re.compile(r"^([A-Z]{2})-([A-Z]+)(\d)(\d+)([A-Z]+)?$")
        try:
            if RE_ROOM.match(trivia[0]):
                room = trivia.pop(0)
            else:
                room = None
            birthday = trivia.pop()
            major = trivia.pop()
            address = "\n".join(trivia)
        except IndexError:
            room = None
            birthday = None
            major = None
            address = None

        # Split up room number
        if room:
            result = RE_ROOM.search(room)
            building_code, entryway, floor, suite, room_number = result.groups()
        else:
            building_code = None
            entryway = None
            floor = None
            suite = None
            room_number = None

        student = Student(
            forename=forename,
            surname=surname,
            year=int(container.find("div", {"class": "student_year"}).text.replace("'", "20")),
            college=college,
            pronoun=container.find("div", {"class": "student_info_pronoun"}).text,
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
        )
        db.session.add(student)

    db.session.commit()
