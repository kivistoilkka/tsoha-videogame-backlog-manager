from app import app
from flask import render_template, request, redirect, abort
import services.users as users
import services.games as games
import services.platforms as platforms
import services.game_collections as game_collections
import services.game_reviews as game_reviews

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template(
                "error.html",
                message="Wrong username or password",
                previous="/login"
            )

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if not username or not password1 or not password2:
            return render_template(
                "error.html",
                message="Some of the fields are missing",
                previous="/register"
            )
        if " " in username or " " in password1 or " " in password2:
            return render_template(
                "error.html",
                message="Username and password cannot contain whitespaces",
                previous="/register"
            )
        if len(username) > 31:
            return render_template(
                "error.html",
                message="Username too long, use less than 32 characters",
                previous="/register"
            )
        if len(password1) > 63 or len(password2) > 63:
            return render_template(
                "error.html",
                message="Password too long, use less than 64 characters",
                previous="/register"
            )
        if len(username) < 5 or len(password1) < 5:
            return render_template(
                "error.html",
                message="Username and/or password too short, use at least 5 characters in each",
                previous="/register"
            )
        if password1 != password2:
            return render_template(
                "error.html",
                message="Passwords do not match",
                previous="/register"
            )
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template(
                "error.html",
                message="Registration failed, try choosing a different username",
                previous="/register"
            )

@app.route("/listings")
def listings():
    all_games = games.get_visible_games_with_review_info()
    reviews = game_reviews.get_review_numbers_averages()
    ratings = game_reviews.get_averages_review_numbers()
    return render_template(
        "listings.html",
        games=all_games,
        reviews=reviews,
        ratings=ratings)

@app.route("/admin")
def admin():
    if not users.is_admin():
        abort(403)
    if request.method == "GET":
        return render_template("admin.html")

@app.route("/admin/games", methods=["GET", "POST"])
def admin_games():
    if not users.is_admin():
        abort(403)
    if request.method == "GET":
        visible_platforms = platforms.get_visible_platforms()
        all_games = games.get_all_games()
        return render_template(
            "admin_games.html",
            platforms=visible_platforms,
            all_games=all_games)
    if request.method == "POST":
        token = request.form["csrf_token"]
        if not users.csrf_token_ok(token):
            abort(403)
        if request.form["operation"] == "add_game":
            name = request.form["name"]
            platform_id = request.form["platform_id"]
            if games.add_game(name, platform_id):
                return redirect("/admin/games")
            return render_template(
                "error.html",
                message="Game addition failed",
                previous="/admin/games"
            )
        if request.form["operation"] == "set_visibility":
            game_id = request.form["game_id"]
            current_visibility = request.form["current_visibility"]
            if current_visibility == "True":
                if games.set_game_hidden(game_id):
                    return redirect("/admin/games")
                return render_template(
                    "error.html",
                    message="Visibility change failed",
                    previous="/admin/games"
                )
            if current_visibility == "False":
                if games.set_game_visible(game_id):
                    return redirect("/admin/games")
                return render_template(
                    "error.html",
                    message="Visibility change failed",
                    previous="/admin/games"
                )
        return render_template(
            "error.html",
            message="Unknown operation",
            previous="/admin/games"
        )

@app.route("/admin/platforms", methods=["GET", "POST"])
def admin_platforms():
    if not users.is_admin():
        abort(403)
    if request.method == "GET":
        all_platforms = platforms.get_all_platforms()
        return render_template("admin_platforms.html", platforms=all_platforms)
    if request.method == "POST":
        token = request.form["csrf_token"]
        if not users.csrf_token_ok(token):
            abort(403)
        if request.form["operation"] == "add_platform":
            name = request.form["name"]
            if platforms.add_platform(name):
                return redirect("/admin/platforms")
            return render_template(
                "error.html",
                message="Platform addition failed",
                previous="/admin/platforms"
            )
        if request.form["operation"] == "set_visibility":
            platform_id = request.form["platform_id"]
            current_visibility = request.form["current_visibility"]
            if current_visibility == "True":
                if platforms.set_platform_hidden(platform_id):
                    return redirect("/admin/platforms")
                return render_template(
                    "error.html",
                    message="Visibility change failed",
                    previous="/admin/platforms"
                )
            if current_visibility == "False":
                if platforms.set_platform_visible(platform_id):
                    return redirect("/admin/platforms")
                return render_template(
                    "error.html",
                    message="Visibility change failed",
                    previous="/admin/platforms"
                )
        return render_template(
            "error.html",
            message="Unknown operation",
            previous="/admin/platforms"
        )

@app.route("/collection/<int:id>", methods=["GET", "POST"])
def collection(id):
    allow = False
    this_user = users.is_user() and users.user_id() == id
    if users.is_admin():
        allow = True
    elif this_user:
        allow = True
    if not allow:
        abort(403)

    if request.method == "GET":
        own_collection = game_collections.get_visible_games(id)
        visible_games = games.get_visible_games()
        return render_template(
            "collection.html",
            collection=own_collection,
            games=visible_games,
            user_id=id,
            this_user=this_user
        )
    if request.method == "POST":
        token = request.form["csrf_token"]
        if not users.csrf_token_ok(token):
            abort(403)
        game_id = request.form["game_id"]
        story_completed = request.form["story_completed"]
        full_completion = request.form["full_completion"]
        if game_collections.add_item(game_id, story_completed, full_completion):
            return redirect("/collection/"+str(id))
        return render_template(
            "error.html",
            message="Game addition failed",
            previous="/collection/"+str(id)
        )

#TODO: refactor as possible POST action to main /collection/id
@app.route("/collection/<int:id>/set_hidden", methods=["POST"])
def collection_set_hidden(id):
    this_user = users.is_user() and users.user_id() == id
    if not this_user:
        abort(403)
    token = request.form["csrf_token"]
    if not users.csrf_token_ok(token):
        abort(403)
    game_id = request.form["game_id"]
    if game_collections.hide_from_collection(game_id):
        return redirect("/collection/"+str(id))
    return render_template(
        "error.html",
        message="Hidding game from collection failed",
        previous="/collection/"+str(id)
    )

@app.route("/reviews/<int:id>", methods=["GET", "POST"])
def reviews_game(id):
    if request.method == "GET":
        game_info = games.get_game_info(id)
        reviews = game_reviews.get_reviews(id)
        if game_info:
            return render_template(
                "game_reviews.html",
                game_id = id,
                game_name=game_info[0],
                platform_name=game_info[1],
                reviews=reviews
            )
        return render_template(
            "error.html",
            message="Game reviews not found",
            previous="/"
        )

    if request.method == "POST":
        token = request.form["csrf_token"]
        if not users.csrf_token_ok(token):
            abort(403)
        if request.form["operation"] == "add_review":
            game_id = request.form["game_id"]
            rating = request.form["rating"]
            comments = request.form["comments"]
            if not int(rating) or int(rating) < 0 or int(rating) > 5:
                return render_template(
                    "error.html",
                    message="Rating value missing or not integer in range 0-5",
                    previous="/reviews/"+str(id)
                )
            if len(comments) > 200:
                return render_template(
                    "error.html",
                    message="Comments too long, use less than 201 characters",
                    previous="/reviews/"+str(id)
                )
            if game_reviews.add_review(game_id, rating, comments):
                return redirect("/reviews/"+str(id))
            return render_template(
                "error.html",
                message="Review addition failed",
                previous="/reviews/"+str(id)
            )
        if request.form["operation"] == "hide_review":
            review_id = request.form["review_id"]
            if game_reviews.set_review_hidden(review_id):
                    return redirect("/reviews/"+str(id))
            return render_template(
                "error.html",
                message="Review deletion failed",
                previous="/reviews/"+str(id)
            )