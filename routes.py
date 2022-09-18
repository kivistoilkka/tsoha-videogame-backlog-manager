from app import app
from flask import render_template, request, redirect, abort
import users, games, platforms

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
    all_games = games.get_all_games()
    return render_template("listings.html", games=all_games)

@app.route("/admin")
def admin():
    if users.is_admin() == False:
        abort(403)
    if request.method == "GET":
        return render_template("admin.html")

@app.route("/admin/games", methods=["GET", "POST"])
def admin_games():
    if users.is_admin() == False:
        abort(403)
    if request.method == "GET":
        visible_platforms = platforms.get_visible_platforms()
        return render_template("admin_games.html", platforms=visible_platforms)
    if request.method == "POST":
        token = request.form["csrf_token"]
        if users.csrf_token_ok(token) == False:
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
    if users.is_admin() == False:
        abort(403)
    if request.method == "GET":
        all_platforms = platforms.get_all_platforms()
        return render_template("admin_platforms.html", platforms=all_platforms)
    if request.method == "POST":
        token = request.form["csrf_token"]
        if users.csrf_token_ok(token) == False:
            abort(403)
        name = request.form["name"]
        if platforms.add_platform(name):
            return redirect("/admin/platforms")
        return render_template(
            "error.html",
            message="Platform addition failed",
            previous="/admin/platforms"
        )