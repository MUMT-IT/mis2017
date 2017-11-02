from main import db
from sqlalchemy.dialects.postgresql import JSON

class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    firstname_en = db.Column(db.String(60))
    lastname_en = db.Column(db.String(60))
    firstname_th = db.Column(db.String(60))
    lastname_th = db.Column(db.String(60))
    email = db.Column(db.String(60))
    gender = db.Column(db.Integer)
    dob = db.Column(db.DateTime)


class LogIn(db.Model):
    __tablename__ = 'logins'
    id = db.Column(db.Integer, primary_key=True)
    credentials = db.Column(JSON)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))
    person = db.relationship("Person", uselist=False)


