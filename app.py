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

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/get_bookings", methods=["GET", "POST"])
def get_bookings():
    bookings = list(mongo.db.bookings.find())
    return render_template("bookings.html", bookings=bookings)


@app.route("/delete_booking/<booking_id>")
def delete_booking(booking_id):
    mongo.db.bookings.remove({"_id": ObjectId(booking_id)})
    flash("Booking Successfully Deleted")
    return redirect(url_for("get_bookings"))


@app.route("/clients", methods=["GET", "POST"])
def get_clients():
    clients = list(mongo.db.clients.find())
    return render_template("clients.html", clients=clients)


@app.route("/search_clients", methods=["GET", "POST"])
def search_clients():
    query = request.form.get("query")
    clients = list(mongo.db.clients.find({"$text": {"$search": query}}))
    return render_template("clients.html", clients=clients)


@app.route("/add_client", methods=["GET", "POST"])
def add_client():
    if request.method == "POST":
        marketing_consent = "on" if request.form.get("marketingConsent") else "off"
        client = {
            "first_name": request.form.get("firstName"),
            "last_name": request.form.get("lastName"),
            "email": request.form.get("email"),
            "mobile": request.form.get("mobile"),
            "marketing_consent": marketing_consent,
            "created_by": session["user"]
        }
        mongo.db.clients.insert_one(client)
        flash("Client Successfully Added")
        return redirect(url_for("get_clients"))

    return render_template("clients.html")


@app.route("/delete_client/<client_id>")
def delete_client(client_id):
    mongo.db.clients.remove({"_id": ObjectId(client_id)})
    flash("Client Successfully Deleted")
    return redirect(url_for("get_clients"))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("signup"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile"))
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
