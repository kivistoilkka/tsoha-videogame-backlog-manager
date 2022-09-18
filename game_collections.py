from db import db
import users

def get_visible_games(id):
    sql = "SELECT G.name, P.name, C.story_completed, C.full_completion \
        FROM collection_items C, games G, platforms P, users U \
        WHERE C.user_id=U.id AND C.game_id=G.id AND G.platform_id=P.id AND C.user_id=:id \
        AND C.visible=TRUE ORDER BY G.name"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()

def add_item(game_id, story_completed, full_completion):
    user_id = users.user_id()
    if not user_id:
        return False
    try:
        sql = "INSERT INTO collection_items \
            (user_id, game_id, story_completed, full_completion, visible) \
            VALUES (:user_id, :game_id, :story_completed, :full_completion, TRUE)"
        db.session.execute(
            sql,
            {
                "user_id": user_id,
                "game_id": game_id,
                "story_completed": story_completed,
                "full_completion": full_completion
            }
        )
        db.session.commit()
        return True
    except:
        return False