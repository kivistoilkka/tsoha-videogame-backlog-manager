from db import db
import services.users as users

def get_reviews(id):
    sql = "SELECT R.rating, R.comments, U.username, R.review_added \
        FROM game_reviews R, games G, users U \
        WHERE R.user_id=U.id AND R.game_id=G.id AND R.game_id=:id \
        AND R.visible=TRUE ORDER BY R.review_added"
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