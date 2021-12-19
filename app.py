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
    return render_template("index.html")

@app.route("/courses")
def courses():
    result = db.session.execute("SELECT name FROM courses")
    re2=db.session.execute("select professor from courses")
    messages = result.fetchall()
    msg2=re2.fetchall()
    return render_template("courses.html",items=messages)

@app.route("/registration")
def registration():
    choices=["Student", "Teacher"]
    return render_template("registration.html", choices=choices)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user==None:
        return redirect("/")
    else:
        hash_value=user[0]
        if check_password_hash(hash_value, password):
            session["username"]=username
            session["role"]=role
        else:
            return redirect("/")
    return redirect("/")