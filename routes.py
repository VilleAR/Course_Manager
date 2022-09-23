from app import app
from flask import redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures import MultiDict
from db import db 
from util import check, is_teacher



@app.route("/test")
def test():
    if session["role"]=="Teacher":
        return render_template("index.html")
    elif session["role"]=="Student":
        return render_template("badlogin.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/courses")
def courses():
    result = db.session.execute("SELECT name, professor FROM courses")
    re2=db.session.execute("select professor from courses")
    messages = result.fetchall()
    ms=[]
    for m in messages:
        ms.append(m)
    return render_template("courses.html",items=ms)

@app.route("/courses/<string:name>")
def indcourse(name):
    sql=("SELECT name, professor, prerequisites FROM courses WHERE name=:name;")
    result=db.session.execute(sql, {"name":name})
    result=result.fetchone()
    if not result:
        return("No course with this name exists!")
    crs=[]
    for num in result[2]:
        sql=("SELECT name FROM courses WHERE id=:num;")
        result2=db.session.execute(sql, {"num":num})
        result2=result2.fetchone()
        crs.append(result2)
    count=len(crs)
    arr=[]
    tier=crs 
    inc=[]
    while tier:
        new=[]
        for i in tier:
            s=str(i[0])
            sql=("SELECT prerequisites FROM courses WHERE name=:s;")
            re=db.session.execute(sql,{"s":s})
            re=re.fetchone()
            #print(re)
            if re:
                for r in re:
                    if r:
                        new.append(r[0])
        tier=[]
        #print(new)
        for n in new:
            sql=("SELECT name FROM courses WHERE id=:n;")
            re=db.session.execute(sql,{"n":n})
            re=re.fetchone()
            re=re[0]
            sql=("SELECT prerequisites FROM courses WHERE name=:s;")
            pres=db.session.execute(sql,{"s":s})
            pres=pres.fetchone()
            if re not in inc:
                tier.append(re)
                inc.append(re)
        #print(new)
        print(tier)
        if len(tier)>=1:
            arr.append(tier)
    arr.reverse()
    newc=[]
    for i in crs:
        if i[0] not in inc:
            newc.append(i[0])
    arr.append(newc)
    print(arr)
    
    return render_template("indcourse.html",course=result,crs=crs,count=count,name=name,arr=arr)

@app.route("/mycourses")
def mycourses():
    if not session:
        flash('Must be logged in to view that page!')
        return redirect("/")
    if session["role"]=="Teacher":
        t=session["username"]
        sql=("SELECT name FROM courses WHERE professor=:t;")
        res=db.session.execute(sql,{"t":t})
        res=res.fetchall()
        return render_template("mycourses.html", crs=res)
    if session["role"]=="Student":
        s=session["username"]
        sql=("SELECT 1 FROM courselists WHERE username=:s")
        res=db.session.execute(sql,{"s":s})
        res=res.fetchall()
        m=1
        if not res:
            m=0
            #print("notres1")
        sql=("SELECT courses FROM courselists WHERE username=:s;")
        res=db.session.execute(sql,{"s":s})
        res=res.fetchone()
        if not res:
            res=[1,2]
        count=0
        if m==1 and res[0]:
            count=1
            #print("!")
        sql="SELECT name FROM courses;"
        result=db.session.execute(sql)
        
        return render_template("courselist.html",crs=res[0],made=m, count=count, items=result)

@app.route("/createplan")
def createplan():
    u=session["username"]
    e=[]
    sql="INSERT INTO courselists (username, courses) VALUES (:u, :e)"
    db.session.execute(sql,{"u":u,"e":e})
    db.session.commit()
    flash('Course plan created')
    return redirect("/mycourses")

@app.route("/addtoplan", methods=["POST"])
def addtoplan():
    toadd=request.form["toadd"]
    u=session["username"]
    sql="SELECT courses FROM courselists WHERE username=:u"
    re=db.session.execute(sql,{"u":u})
    re=re.fetchone()
    t=True
    for r in re[0]:
        if r==toadd:
            t=False
    if t:
        sql="SELECT prerequisites FROM courses WHERE name=:toadd"
        re2=db.session.execute(sql,{"toadd":toadd})
        re2=re2.fetchone()
        for r in re2[0]:
            if r in re:
                t=False 
        if t:
            sql="UPDATE courselists SET courses=array_append(courses, :toadd) WHERE username=:u;"
            db.session.execute(sql,{"toadd":toadd, "u":u})
            db.session.commit()
            flash('Course added to plan')
        else:
            flash('Add prerequisites to plan first!')
    else:
        flash('Course already in plan!')
    return redirect("/mycourses")

@app.route("/addnew")
def addnew():
    sql=("SELECT name FROM courses;")
    result=db.session.execute(sql)

    return render_template("addnew.html",items=result)

@app.route("/create", methods=["POST"])
def create():
    coursename=request.form["coursename"]
    professor=request.form["professor"]
    if not check(coursename) or not check(professor):
        return redirect("/badlogin")
    prereqs=request.form.to_dict(flat=False)
    if not "prereqs" in prereqs:
        prerequisites=[]
        #print("no")
    else:   
        #print(prereqs["prereqs"])
        prereqs=prereqs["prereqs"]
        reqsarr=[]
        for name in prereqs:
            sql=("SELECT id FROM courses WHERE name=:name;")
            result=db.session.execute(sql, {"name":name})
            reqsarr.append(int(result.fetchone()[0]))
        prerequisites=reqsarr
    name=coursename
    sql=("SELECT name, id FROM courses;")
    result=db.session.execute(sql)
    result=result.fetchall()
    #print(result)
    newid=0
    toadd=True
    for i in result:
        t=str(i[0])
        #print(t)
        if coursename==t:
            error = 'Course with this name already exists!'
            toadd=False
        q=int(i[1])
        if q>newid:
            newid=q

    newid+=1
    if toadd:
        sql="INSERT INTO courses (id, name, professor, prerequisites) VALUES (:id, :name, :professor, :prerequisites)"
        db.session.execute(sql, {"id":newid, "name":name,"professor":professor,"prerequisites":prerequisites})
        db.session.commit()
        flash('Course created')
       
    else:
        flash('Course creation failed: course with this name already exists')
        return redirect("/addnew")
        

    return redirect("/courses")

@app.route("/delete",methods=["POST"])
def delete():
    name=request.form["name"]
    sql="SELECT id FROM courses WHERE name=:name"
    result=db.session.execute(sql, {"name":name})
    n=result.fetchone()[0]
    sql="DELETE FROM courses WHERE name=:name"
    db.session.execute(sql, {"name":name})
    db.session.commit()
    sql="SELECT id, prerequisites FROM courses;"
    result=db.session.execute(sql)
    res=result.fetchall()
    for r in res:
        #r[0]=id, r[1]=prerequisites
        if n in r[1]:
            arr=r[1]
            arr.remove(n)
            #print(arr)
            i=r[0]
            sql="UPDATE courses SET prerequisites=:arr WHERE id=:id;"
            db.session.execute(sql,{"arr":arr,"id":i})
            db.session.commit()


    
    s="Course '"+str(name)+"' deleted"
    flash(s)
    
    return redirect("/courses")
    
@app.route("/professors")
def professors():
    sql="SELECT professor FROM courses"
    result=db.session.execute(sql)
    res=result.fetchall()
    return render_template("professors.html",professors=res)

@app.route("/professors/<string:profn>")
def prof(profn):
    sql="SELECT name FROM courses WHERE professor=:profn;"
    result=db.session.execute(sql, {"profn":profn})
    result=result.fetchall()
    if not result:
        return("Professor has no courses")
    else:
        return render_template("indprof.html", crs=result, profn=profn)

@app.route("/registration")
def registration():
    choices=["Student", "Teacher"]
    return render_template("registration.html", choices=choices)

@app.route("/register", methods=["POST"])
def register():
    username=request.form["username"]
    password=request.form["password"]
    role=request.form["role"]
    sql="SELECT username FROM users"
    re=db.session.execute(sql)
    re=re.fetchall()
    taken=False
    for r in re:
        if r[0]==username:
            taken=True
           
    if username=="" or password=="" or role=="":
        return redirect("/registration")
    elif not check(username):
        return redirect("/badlogin")
    elif taken:
        flash("User with this name already exists")
        return redirect("/registration")
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