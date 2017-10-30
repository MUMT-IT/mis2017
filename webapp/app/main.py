from flask import Flask, render_template
from auth import auth as auth_blueprint

app = Flask(__name__)

app.register_blueprint(auth_blueprint)

@app.route('/')
def main():
    return render_template("main.html")


if __name__ == '__main__':
    app.run(debug=True)