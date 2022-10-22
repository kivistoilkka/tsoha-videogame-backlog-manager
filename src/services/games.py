from db import db

def get_visible_games():
    sql = "SELECT G.id, G.name, P.name FROM games G, platforms P \
        WHERE G.platform_id=P.id AND G.visible=TRUE AND P.visible=TRUE \
        ORDER BY G.name"
    result = db.session.execute(sql)
    return result.fetchall()

def get_visible_games_with_review_info():
    sql = "SELECT G.id, G.name AS game_name, P.name AS platform_name, \
        COUNT(R.rating) AS reviews, COALESCE(AVG(R.rating),-1) as review_average \
        FROM games G \
        LEFT JOIN (SELECT * FROM game_reviews WHERE visible=TRUE) R ON G.id=R.game_id \
        JOIN platforms P ON G.platform_id=P.id \
        WHERE G.visible=TRUE AND P.visible=TRUE \
        GROUP BY G.id, G.name, P.name \
        ORDER BY game_name, platform_name;"
    result = db.session.execute(sql)
    return result.fetchall()

def get_all_games():
    sql = "SELECT G.id, G.name, P.name, G.visible, P.visible FROM games G, platforms P \
        WHERE G.platform_id=P.id ORDER BY G.name"
    result = db.session.execute(sql)
    return result.fetchall()

def add_game(name, platform_id):
    if game_in_database_and_visible(name, platform_id):
        return False
    try:
        sql = "INSERT INTO games (name, platform_id, visible) \
            VALUES (:name, :platform_id, TRUE)"
        db.session.execute(sql, {"name": name, "platform_id": platform_id})
        db.session.commit()
        return True
    except:
        return False

def game_in_database_and_visible(name, platform_id):
    sql = "SELECT 1 FROM games G, platforms P \
        WHERE G.platform_id=P.id AND \
        UPPER(G.name)=:name AND G.platform_id=:platform_id \
        AND G.visible=TRUE AND P.visible=TRUE"
    result = db.session.execute(sql, {"name":name.upper(), "platform_id":platform_id})
    if result.fetchone():
        return True
    return False

def get_game_info(id):
    sql = "SELECT G.name, P.name FROM games G, platforms P \
        WHERE G.platform_id=P.id AND G.visible=TRUE AND P.visible=TRUE AND G.id=:id"
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()

def set_game_hidden(id):
    try:
        sql = "UPDATE games SET visible=FALSE WHERE id=:id"
        db.session.execute(sql, { "id": id })
        db.session.commit()
        return True
    except:
        return False

def set_game_visible(id):
    try:
        sql = "UPDATE games SET visible=TRUE WHERE id=:id"
        db.session.execute(sql, { "id": id })
        db.session.commit()
        return True
    except:
        return False