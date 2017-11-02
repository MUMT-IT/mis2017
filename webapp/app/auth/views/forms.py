from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class UserRegisterForm(FlaskForm):
    # firstname_th = StringField('Thai first name', validators=[Required()])
    # lastname_th = StringField('Thai last name', validators=[Required()])
    firstname_en = StringField('English first name')
    lastname_en = StringField('English last name')
    email = StringField('Email')
    submit = SubmitField('Submit')


class LogInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])