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
    if game_in_database(name, platform_id):
        return False
    try:
        sql = "INSERT INTO games (name, platform_id, visible) \
            VALUES (:name, :platform_id, TRUE)"
        db.session.execute(sql, {"name": name, "platform_id": platform_id})
        db.session.commit()
        return True
    except:
        return False

def game_in_database(name, platform_id):
    #TODO: check with lowercase names
    sql = "SELECT 1 FROM games WHERE name=:name AND platform_id=:platform_id"
    result = db.session.execute(sql, {"name":name, "platform_id":platform_id})
    if result.fetchone():
        return True
    return False

#TODO: set_game_hidden
#TODO: set_game_visible