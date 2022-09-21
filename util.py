from db import db


def check(n):
    if "'" in n or "(" in n or ")" in n or "=" in n or "_" in n: #spaghetti
        return False
    return True

def is_teacher(username):
    sql=("SELECT role FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    content=result.fetchone()[0]
    if content=="Teacher":
        return False 
    else:
        return True