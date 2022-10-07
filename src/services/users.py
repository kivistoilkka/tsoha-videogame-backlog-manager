import secrets
from db import db
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, is_admin) \
            VALUES (:username, :password, FALSE)"
        db.session.execute(
            sql,
            {"username": username, "password": hash_value}
        )
        db.session.commit()
    except:
        return False
    return login(username, password)

def login(username, password):
    sql = "SELECT id, password, is_admin FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = username
        session["admin_link_visible"] = user.is_admin
        session["csrf_token"] = secrets.token_hex(16)
        return True
    return False

def logout():
    del session["user_id"]
    del session["username"]
    del session["admin_link_visible"]
    del session["csrf_token"]

def is_admin():
    id = user_id()
    sql = "SELECT 1 FROM users WHERE id=:user_id AND is_admin=TRUE"
    result = db.session.execute(sql, {"user_id":id})
    if result.fetchone():
        return True
    return False

def csrf_token_ok(token):
    return session["csrf_token"] == token

def is_user():
    id = user_id()
    sql = "SELECT 1 FROM users WHERE id=:user_id"
    result = db.session.execute(sql, {"user_id":id})
    if result.fetchone():
        return True
    return False

def user_id():
    return session.get("user_id", 0)