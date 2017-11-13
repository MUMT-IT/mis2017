import os
from flask_login import LoginManager, current_user
from flask import Flask, render_template, session, request, redirect
# from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from flask_script import Manager
import models

app = Flask(__name__)
app.secret_key = 'flasky'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'postgresql+psycopg2://likit@localhost:5432/mumtmis_dev'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MONGODB_SETTINGS'] = {
    'db': 'mis_test',
}

manager = Manager(app)

db = MongoEngine(app)

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.main'

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from account import account as account_blueprint
app.register_blueprint(account_blueprint)


@login_manager.user_loader
def load_user(user_id):
    return models.User.objects.get(id=user_id)


@app.before_request
def before_request():
    if 'language' not in session:
        session['language'] = 'en'


def switch_lang():
    if session['language'] == 'en':
        session['language'] = 'th'
    else:
        session['language'] = 'en'

    if current_user and current_user.is_authenticated:
        current_user.language = session['language']
        current_user.save()


@app.route('/')
def main():
    return render_template("%s/base.html" % session['language'])


@app.route('/switchlanguage')
def switch_web_language():
    switch_lang()
    return redirect(request.referrer)



if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # app.run(debug=True, host="0.0.0.0", port=5000)
    manager.run()