from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

def check(n):
    if "'" in n or "(" in n or ")" in n or "=" in n or "_" in n: #spaghetti
        return False
    return True

@app.route("/ist")
def is_teacher(username):
    
    sql=("SELECT role FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    content=result.fetchone()[0]
    if content=="Teacher":
        return False 
    else:
        return True
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

@app.route("/register", methods=["POST"])
def register():
    username=request.form["username"]
    password=request.form["password"]
    role=request.form["role"]
    
    if username=="" or password=="" or role=="":
        return redirect("/registration")
    elif not check(username):
        return redirect("/badlogin")
    else:
        hash_value = generate_password_hash(password)
        
        sql = "INSERT INTO users (username,password, role) VALUES (:username,:password, :role)"
        db.session.execute(sql, {"username":username,"password":hash_value, "role":role})
        db.session.commit()
        return redirect("/")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if username=="" or password=="":
        return redirect("/")
    elif not check(username) or not check(password):
        return redirect("/badlogin")
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    
    if user==None:
        return redirect("/")
    else:
        hash_value=user[0]
        sql2="SELECT role FROM users WHERE username=:username"
        result2 = db.session.execute(sql2, {"username":username})
        role=result2.fetchone()[0]
        if check_password_hash(hash_value, password):
            session["username"]=username
            session["role"]=role
        else:
            return redirect("/badlogin")
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    del session["role"]
    return redirect("/")

@app.route("/badlogin")
def badlogin():
    return render_template("badlogin.html")