from db import db
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, is_admin) VALUES (:username, :password, :is_admin)"
        db.session.execute(
            sql,
            {"username": username, "password": hash_value, "is_admin": False}
        )
        db.session.commit()
    except:
        return False
    return login(username, password)

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = username
        print("Login ok")
        return True
    return False

def logout():
    del session["user_id"]
    del session["username"]