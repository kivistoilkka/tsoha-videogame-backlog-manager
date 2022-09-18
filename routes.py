from app import app
from flask import render_template, request, redirect
import users, games

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
    return render_template("listings.html", all_games=all_games)