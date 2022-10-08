from db import db
import services.users as users

def get_visible_games(id):
    sql = "SELECT G.id, G.name, P.name, C.story_completed, C.full_completion \
        FROM collection_items C, games G, platforms P, users U \
        WHERE C.user_id=U.id AND C.game_id=G.id AND G.platform_id=P.id AND C.user_id=:id \
        AND C.visible=TRUE ORDER BY G.name"
    result = db.session.execute(sql, { "id":id })
    return result.fetchall()

def add_item(game_id, story_completed, full_completion):
    user_id = users.user_id()
    if not user_id:
        return False
    if game_in_collection(user_id, game_id):
        return set_visible_and_update(game_id, story_completed, full_completion)
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

def game_in_collection(user_id, game_id):
    sql = "SELECT 1 FROM collection_items WHERE user_id=:user_id AND game_id=:game_id"
    result = db.session.execute(sql, { "user_id":user_id, "game_id":game_id })
    if result.fetchone():
        return True
    return False

def hide_from_collection(game_id):
    user_id = users.user_id()
    if not user_id:
        return False
    try:
        sql = "UPDATE collection_items SET visible=FALSE WHERE user_id=:user_id AND game_id=:game_id"
        db.session.execute(sql, { "user_id": user_id, "game_id": game_id })
        db.session.commit()
        return True
    except:
        return False

def set_visible_and_update(game_id, story_completed, full_completion):
    user_id = users.user_id()
    if not user_id:
        return False
    try:
        sql = "UPDATE collection_items \
            SET visible=TRUE, \
            story_completed=:story_completed, \
            full_completion=:full_completion \
            WHERE user_id=:user_id AND game_id=:game_id"
        db.session.execute(sql,             {
                "user_id": user_id,
                "game_id": game_id,
                "story_completed": story_completed,
                "full_completion": full_completion
            })
        db.session.commit()
        print("Onnistui!")
        return True
    except:
        print("Epäonnistui!")
        return False