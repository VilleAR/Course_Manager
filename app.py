from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

def func(n):
    return (n**2)+5*n+17
@app.route("/")
def index():
    return str(func(10))

@app.route("/courses")
def courses():
    result = db.session.execute("SELECT prerequisites FROM courses")
    messages = result.fetchone()[0]
    return render_template("courses.html")
 