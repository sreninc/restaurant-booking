import os
from datetime import datetime
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
    clients = list(mongo.db.clients.find(
        {},
        {"first_name": 1, "last_name": 1}))
    print(clients)
    for x in range(len(bookings)):
        new_date = datetime.strptime(bookings[x]["date"], '%Y-%m-%d')
        bookings[x]["new_date"] = new_date.strftime("%a %d %b")
        for y in range(len(clients)):
            if str(clients[y]["_id"]) == str(bookings[x]["client_id"]):
                bookings[x]["new_client_id"] = clients[y]["first_name"] + " " + clients[y]["last_name"]
    return render_template("bookings.html", bookings=bookings, clients=clients)


@app.route("/add_booking", methods=["GET", "POST"])
def add_booking():
    if request.method == "POST":
        if request.form.get("status") == "completed":
            bookings_completed = 1
        else:
            bookings_completed = 0
        # find the client
        client = mongo.db.clients.find_one(
            {"_id": ObjectId(request.form.get("clientId"))}
        )
        # update the client
        if request.form.get("booking_id"):
            mongo.db.clients.update(
                    {"_id": ObjectId(request.form.get("clientId"))},
                    {"$set": {
                        "bookings_completed": client["bookings_completed"] + int(bookings_completed),
                        "value": client["value"] + int(request.form.get("value"))
                        }
                    }
                )
        else:
            mongo.db.clients.update(
                {"_id": ObjectId(request.form.get("clientId"))},
                {"$set": {
                    "bookings": client["bookings"] + 1,
                    "bookings_completed": client["bookings_completed"] + int(bookings_completed),
                    "value": client["value"] + int(request.form.get("value"))
                    }
                }
            )
        booking = {
            "client_id": request.form.get("clientId"),
            "date": request.form.get("date"),
            "time": request.form.get("time"),
            "people": request.form.get("people"),
            "status": request.form.get("status"),
            "value": request.form.get("value"),
            "created_by": session["email"]
        }
        mongo.db.bookings.insert_one(booking)
        flash("Booking Successfully Added")
        return redirect(url_for("get_bookings"))

    return render_template("bookings.html")


@app.route("/delete_booking/<booking_id>/<client_id>/<booking_value>/<booking_status>")
def delete_booking(booking_id, client_id, booking_value, booking_status):
    # find the client
    client = mongo.db.clients.find_one({"_id": ObjectId(client_id)})
    if booking_status == "completed":
        bookings_completed = 1
    else:
        bookings_completed = 0
    # update the client
    mongo.db.clients.update(
                {"_id": ObjectId(client_id)},
                {"$set": {
                    "bookings": client["bookings"] - 1,
                    "value": client["value"] - int(booking_value),
                    "bookings_completed": client["bookings_completed"] - int(bookings_completed)
                    }
                }
            )
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
        marketing_consent = "on" if request.form.get("add-client-marketing") else "off"
        client = {
            "first_name": request.form.get("add-client-firstname").capitalize(),
            "last_name": request.form.get("add-client-lastname"),
            "email": request.form.get("add-client-email").lower(),
            "mobile": request.form.get("add-client-mobile"),
            "marketing_consent": marketing_consent,
            "bookings": 0,
            "bookings_completed": 0,
            "value": 0,
            "created_by": session["email"],
            "created_date": datetime.today()
        }
        mongo.db.clients.insert_one(client)
        flash("Client Successfully Added")
        return redirect(url_for("get_clients"))

    return render_template("clients.html")


@app.route("/edit_client", methods=["GET", "POST"])
def edit_client():
    if request.method == "POST":
        marketing_consent = "on" if request.form.get("edit-client-marketing") else "off"
        mongo.db.clients.update(
                {"_id": ObjectId(request.form.get("editClient"))},
                {"$set": {
                    "first_name": request.form.get("edit-client-firstname").capitalize(),
                    "last_name": request.form.get("edit-client-lastname"),
                    "email": request.form.get("edit-client-email").lower(),
                    "mobile": request.form.get("edit-client-mobile"),
                    "marketing_consent": marketing_consent,
                    "updated_by": session["email"],
                    "updated_date": datetime.today()
                    }
                }
            )
        flash("Client Successfully Edited")
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
        # check if email exists in db
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["email"] = request.form.get("email").lower()
                    email = list(mongo.db.users.find({"email": session["email"]}))
                    flash("Welcome, {}".format(
                        request.form.get("email")))
                    return redirect(url_for(
                        "profile", email=email))
            else:
                # invalid password match
                flash("Incorrect Email and/or Password")
                return redirect(url_for("login"))

        else:
            # Email doesn't exist
            flash("Incorrect Email and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<email>", methods=["GET", "POST"])
def profile(email):
    # grab the session user's email from db
    email = mongo.db.users.find_one(
        {"email": session["email"]})["email"]

    if session["email"]:
        user = list(mongo.db.users.find({"email": session["email"]}))
        return render_template("profile.html", user=user)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove email from session cookie
    flash("You have been logged out")
    session.pop("email")
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # check if email already exists in db
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            flash("Email already exists")
            return redirect(url_for("signup"))

        register = {
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "name": request.form.get("name").lower().capitalize(),
            "restaurant_name": request.form.get("restaurant-name").lower().capitalize()
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["email"] = request.form.get("email").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile"))
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
