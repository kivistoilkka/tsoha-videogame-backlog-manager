from platform import platform
from db import db

def get_visible_platforms():
    sql = "SELECT id, name FROM platforms WHERE visible=TRUE ORDER BY name"
    result = db.session.execute(sql)
    return result.fetchall()

def get_all_platforms():
    sql = "SELECT id, name, visible FROM platforms ORDER BY name"
    result = db.session.execute(sql)
    return result.fetchall()
  
def add_platform(name):
    if platform_in_database(name):
        return False
    try:
        sql = "INSERT INTO platforms (name, visible) \
            VALUES (:name, TRUE)"
        db.session.execute(sql, {"name": name})
        db.session.commit()
        return True
    except:
        return False

def platform_in_database(name):
    sql = "SELECT 1 FROM platforms WHERE UPPER(name)=:name"
    result = db.session.execute(sql, { "name":name.upper() })
    if result.fetchone():
        return True
    return False