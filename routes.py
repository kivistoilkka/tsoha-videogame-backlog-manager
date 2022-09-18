from app import app
from flask import render_template, request, redirect, abort
import users, games, platforms, game_collections

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
    all_games = games.get_visible_games()
    return render_template("listings.html", games=all_games)

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
        return render_template("admin_games.html", platforms=visible_platforms)
    if request.method == "POST":
        token = request.form["csrf_token"]
        if not users.csrf_token_ok(token):
            abort(403)
        name = request.form["name"]
        platform_id = request.form["platform_id"]
        if games.add_game(name, platform_id):
            return redirect("/listings")
        return render_template(
            "error.html",
            message="Game addition failed",
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
        name = request.form["name"]
        if platforms.add_platform(name):
            return redirect("/admin/platforms")
        return render_template(
            "error.html",
            message="Platform addition failed",
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
        #TODO: check inputs
        if game_collections.add_item(game_id, story_completed, full_completion):
            return redirect("/collection/"+str(id))
        return render_template(
            "error.html",
            message="Game addition failed",
            previous="/collection/"+str(id)
        )
