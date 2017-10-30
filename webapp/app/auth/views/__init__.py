from flask import render_template
from .. import auth

@auth.route('/')
def main():
    return render_template("auth/main.html")