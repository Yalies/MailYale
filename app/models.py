from app import app, db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String, primary_key=True)
    registered_on = db.Column(db.Integer)
    last_seen = db.Column(db.Integer)
    admin = db.Column(db.Boolean, default=False)
    banned = db.Column(db.Boolean, default=False)
