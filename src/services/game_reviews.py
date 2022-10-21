from db import db
import services.users as users

def get_reviews(id):
    sql = "SELECT R.rating, R.comments, U.username, R.review_added \
        FROM game_reviews R, games G, users U, platforms P \
        WHERE R.user_id=U.id AND R.game_id=G.id AND R.game_id=:id \
        AND R.visible=TRUE AND G.visible=TRUE and P.visible=TRUE \
        ORDER BY R.review_added"
    result = db.session.execute(sql, { "id":id })
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
        AND G.visible=TRUE AND P.visible=TRUE \
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
        AND G.visible=TRUE and P.visible=TRUE \
        GROUP BY G.id, G.name, P.name \
        ORDER BY review_average DESC, reviews DESC \
        LIMIT 5"
    result = db.session.execute(sql)
    return result.fetchall()