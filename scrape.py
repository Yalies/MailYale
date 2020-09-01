import requests
from bs4 import BeautifulSoup
import csv
import re
import os
import time

DEBUG = False

with open('cookie.txt', 'r') as f:
    cookie = f.read().strip()

headers = {
    'Cookie': cookie,
}

filename = 'page.html'
if not os.path.exists(filename):
    print('Page not cached, fetching...')
    params = {
        'currentIndex': -1,
        'numberToGet': 12,
    }
    if not DEBUG:
        params.update({
            'currentIndex': -1,
            'numberToGet': -1,
        })

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
students = []
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
    try:
        room = trivia.pop(0)
        birthday = trivia.pop()
        major = trivia.pop()
        address = "\n".join(trivia)
    except IndexError:
        room = ""
        birthday = ""
        major = ""
        address = ""

    image_id = container.find("div", {"class": "student_img"}).find("img")["src"][len("/facebook/Photo?id="):]
    image_filename = 'images/' + forename + ' ' + surname + '.jpg'
    if not os.path.exists(image_filename):
        image_r = requests.get('https://students.yale.edu/facebook/Photo?id=' + image_id,
                               headers=headers)
        with open(image_filename, 'wb') as f:
            f.write(image_r.content)
        time.sleep(2)

    students.append({
        "forename": forename,
        "surname": surname,
        "image_id": image_id,
        "year": int(container.find("div", {"class": "student_year"}).text.replace("'", "20")),
        "pronoun": container.find("div", {"class": "student_info_pronoun"}).text,
        "email": email,
        "room": room,
        "birthday": birthday,
        "major": major,
        "address": address,
    })

with open("students.csv", "w", encoding="utf-8") as f:
    keys = students[0].keys()
    writer = csv.DictWriter(f, keys)
    writer.writeheader()
    writer.writerows(students)
