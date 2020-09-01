from app import app, db


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer)
    college = db.Column(db.String)
    pronoun = db.Column(db.String)
    email = db.Column(db.String, nullable=False)
    room = db.Column(db.String)
    birthday = db.Column(db.String)
    major = db.Column(db.String)
    address = db.Column(db.String)
