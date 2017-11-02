import os
from flask_login import LoginManager
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
import models

app = Flask(__name__)
app.secret_key = 'flasky'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'postgresql+psycopg2://likit@localhost:5432/mumtmis_dev'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.main'

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

@login_manager.user_loader
def load_user(user_id):
    return models.Person.query.get(user_id)

@app.route('/')
def main():
    return render_template("main.html")


if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    # app.run(debug=True, host="0.0.0.0", port=5000)
    manager.run()