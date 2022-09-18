from db import db

def get_all_games():
    sql = "SELECT G.name, P.name, G.visible FROM games G, platforms P \
        WHERE G.platform_id=P.id ORDER BY G.name"
    result = db.session.execute(sql)
    return result.fetchall()