from db import db

def get_visible_games():
    sql = "SELECT G.id, G.name, P.name FROM games G, platforms P \
        WHERE G.platform_id=P.id AND G.visible=TRUE ORDER BY G.name"
    result = db.session.execute(sql)
    return result.fetchall()

def get_all_games():
    sql = "SELECT G.name, P.name, G.visible FROM games G, platforms P \
        WHERE G.platform_id=P.id ORDER BY G.name"
    result = db.session.execute(sql)
    return result.fetchall()

def add_game(name, platform_id):
    try:
        sql = "INSERT INTO games (name, platform_id, visible) \
            VALUES (:name, :platform_id, TRUE)"
        db.session.execute(sql, {"name": name, "platform_id": platform_id})
        db.session.commit()
        return True
    except:
        return False