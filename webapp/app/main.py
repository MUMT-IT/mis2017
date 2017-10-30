import os
from flask import Flask, render_template
app = Flask(__name__)
app.secret_key = 'flasky'

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

@app.route('/')
def main():
    return render_template("main.html")


if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(debug=True)