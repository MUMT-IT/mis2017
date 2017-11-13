import datetime
from flask_login import UserMixin
from main import db, login_manager
# from sqlalchemy.dialects.postgresql import JSON


class Person(UserMixin, db.Document):
    firstname_en = db.StringField()
    lastname_en = db.StringField()
    firstname_th = db.StringField()
    lastname_th = db.StringField()
    email = db.StringField(maxlength=100, required=True)
    gender = db.IntField()
    dob = db.DateTimeField()


class User(UserMixin, db.Document):
    person = db.ReferenceField(Person)
    logins = db.ListField(db.DateTimeField())
    credentials = db.DictField()
    language = db.StringField()