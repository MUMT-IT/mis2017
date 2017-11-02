import datetime
from flask_login import UserMixin
from main import db, login_manager
from sqlalchemy.dialects.postgresql import JSON

class Person(UserMixin, db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    firstname_en = db.Column(db.String(60))
    lastname_en = db.Column(db.String(60))
    firstname_th = db.Column(db.String(60))
    lastname_th = db.Column(db.String(60))
    email = db.Column(db.String(60))
    gender = db.Column(db.Integer)
    dob = db.Column(db.DateTime)
    login_id = db.Column(db.Integer, db.ForeignKey('logins.id'))
    login = db.relationship("LogIn", uselist=False)


class LogIn(db.Model):
    __tablename__ = 'logins'
    id = db.Column(db.Integer, primary_key=True)
    credentials = db.Column(JSON)
    updatedOn = db.Column(db.DateTime, default=datetime.datetime.now)