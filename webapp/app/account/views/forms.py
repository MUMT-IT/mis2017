from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, Email


class EventCalendar(FlaskForm):
    summary = StringField('Summary')
    location = StringField('Location')
    description = TextAreaField('Description')
    startdate = DateTimeField('Start')
    enddate = DateTimeField('End')
    attendees = StringField('Attendees')
    submit = SubmitField('Submit')