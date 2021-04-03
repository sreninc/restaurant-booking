import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/bookings", methods=["GET", "POST"])
def get_bookings():
    return render_template("bookings.html")


@app.route("/clients", methods=["GET", "POST"])
def get_clients():
    return render_template("clients.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/profile", methods=["GET", "POST"])
def get_profile():
    return render_template("profile.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
