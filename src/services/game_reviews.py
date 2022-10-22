from db import db
import services.users as users

def get_reviews(game_id):
    sql = "SELECT R.rating, R.comments, U.username, R.review_added, R.visible, R.id, U.id \
        FROM game_reviews R, games G, users U, platforms P \
        WHERE R.user_id=U.id AND R.game_id=G.id AND G.platform_id=P.id \
        AND R.game_id=:id \
        AND G.visible=TRUE and P.visible=TRUE \
        ORDER BY R.review_added"
    result = db.session.execute(sql, { "id":game_id })
    return result.fetchall()

def add_review(game_id, rating, comments):
    user_id = users.user_id()
    if not user_id:
        return False
    try:
        sql = "INSERT INTO game_reviews \
            (user_id, game_id, rating, comments, review_added, visible) \
            VALUES (:user_id, :game_id, :rating, :comments, NOW(), TRUE)"
        db.session.execute(
            sql,
            {
                "user_id": user_id,
                "game_id": game_id,
                "rating": rating,
                "comments": comments
            }
        )
        db.session.commit()
        return True
    except:
        return False

def get_review_numbers_averages():
    sql = "SELECT G.id, G.name AS game_name, P.name AS platform_name, \
        COUNT(*) AS reviews, AVG(R.rating) as review_average \
        FROM games G, platforms P, game_reviews R \
        WHERE R.game_id=G.id AND G.platform_id=P.id \
        AND G.visible=TRUE AND P.visible=TRUE AND R.visible=TRUE \
        GROUP BY G.id, G.name, P.name \
        ORDER BY reviews DESC, review_average DESC \
        LIMIT 5"
    result = db.session.execute(sql)
    return result.fetchall()

def get_averages_review_numbers():
    sql = "SELECT G.id, G.name AS game_name, P.name AS platform_name, \
        COUNT(*) AS reviews, AVG(R.rating) as review_average \
        FROM games G, platforms P, game_reviews R \
        WHERE R.game_id=G.id AND G.platform_id=P.id \
        AND G.visible=TRUE and P.visible=TRUE AND R.visible=TRUE \
        GROUP BY G.id, G.name, P.name \
        ORDER BY review_average DESC, reviews DESC \
        LIMIT 5"
    result = db.session.execute(sql)
    return result.fetchall()

def review_by_user(review_id, user_id):
    sql = "SELECT user_id FROM game_reviews WHERE id=:id"
    result = db.session.execute(sql, { "id": review_id }).fetchone()
    if result and result[0] == user_id:
        return True
    return False

def set_review_hidden(review_id):
    user_id = users.user_id()
    if not user_id:
        return False
    if review_by_user(review_id, user_id) or users.is_admin():    
        try:
            sql = "UPDATE game_reviews SET visible=FALSE WHERE id=:id"
            db.session.execute(sql, { "id": review_id })
            db.session.commit()
            return True
        except:
            return False
    return False

def get_all_reviews():
    sql = "SELECT R.review_added, R.visible, U.username, \
        G.id, G.name, P.name, R.rating, R.comments \
        FROM game_reviews R, games G, users U, platforms P \
        WHERE R.user_id=U.id AND R.game_id=G.id AND G.platform_id=P.id \
        AND G.visible=TRUE and P.visible=TRUE \
        ORDER BY R.review_added DESC"
    result = db.session.execute(sql)
    return result.fetchall()