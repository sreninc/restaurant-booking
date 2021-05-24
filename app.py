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
        if request.form.get("add-booking-status") == "completed":
            bookings_completed = 1
        else:
            bookings_completed = 0
        # find the client
        client = mongo.db.clients.find_one(
            {"_id": ObjectId(request.form.get("add-booking-client-id"))}
        )
        # update the client
        mongo.db.clients.update(
            {"_id": ObjectId(request.form.get("add-booking-client-id"))},
            {"$set": {
                "bookings": client["bookings"] + 1,
                "bookings_completed": client["bookings_completed"] + int(bookings_completed),
                "value": client["value"] + int(request.form.get("add-booking-value"))
                }
            }
        )
        booking = {
            "client_id": request.form.get("add-booking-client-id"),
            "date": request.form.get("add-booking-date"),
            "time": request.form.get("add-booking-time"),
            "people": request.form.get("add-booking-people"),
            "status": request.form.get("add-booking-status"),
            "value": request.form.get("add-booking-value"),
            "created_by": session["email"],
            "created_date": datetime.today()
        }
        mongo.db.bookings.insert_one(booking)
        flash("Booking Successfully Added")
        flash("Client Booking Stats Updated")
        return redirect(url_for("get_bookings"))

    return render_template("bookings.html")


@app.route("/edit_booking", methods=["GET", "POST"])
def edit_booking():
    if request.method == "POST":
        # find the client
        client = mongo.db.clients.find_one(
            {"_id": ObjectId(request.form.get("edit-booking-client-id"))}
        )
        booking = mongo.db.bookings.find_one(
            {"_id": ObjectId(request.form.get("edit-booking-id"))}
        )

        value = request.form.get("edit-booking-value")
        bookings_completed = 0
        old_value = 0
        if request.form.get("edit-booking-status") == "completed" and booking["status"] != "completed":
            bookings_completed = 1
        elif request.form.get("edit-booking-status") != "completed" and booking["status"] == "completed":
            old_value = booking["value"]
            value = 0
            bookings_completed = -1
        elif request.form.get("edit-booking-status") == "completed" and booking["status"] == "completed":
            old_value = booking["value"]

        print(booking["value"])
        print(old_value)
        print(value)

        # update the client
        mongo.db.clients.update(
                {"_id": ObjectId(request.form.get("edit-booking-client-id"))},
                {"$set": {
                    "value": client["value"] + int(value) - int(old_value),
                    "bookings_completed": client["bookings_completed"] + int(bookings_completed)
                    }
                }
            )

        # update the booking
        mongo.db.bookings.update(
                {"_id": ObjectId(request.form.get("edit-booking-id"))},
                {"$set": {
                    "date": request.form.get("edit-booking-date"),
                    "time": request.form.get("edit-booking-time"),
                    "people": request.form.get("edit-booking-people"),
                    "status": request.form.get("edit-booking-status"),
                    "value": request.form.get("edit-booking-value"),
                    "updated_by": session["email"],
                    "updated_date": datetime.today()
                    }
                }
            )
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


@app.route("/edit_guest/<guest_id>", methods=["GET", "POST"])
def edit_guest(guest_id):
    if request.method == "POST":
        marketing_consent = "on" if request.form.get("marketingConsent") else "off"
        dob = datetime.strptime(request.form.get("dob"), '%Y-%m-%d') if request.form.get("dob") else ""
        mongo.db.clients.update(
                {"_id": ObjectId(guest_id)},
                {"$set": {
                    "first_name": request.form.get("firstName").capitalize(),
                    "last_name": request.form.get("lastName"),
                    "email": request.form.get("email").lower(),
                    "mobile": request.form.get("mobile"),
                    "dob": dob,
                    "marketing_consent": marketing_consent,
                    "notes": request.form.get("notes"),
                    "updated_by": session["email"],
                    "updated_date": datetime.today()
                    }
                }
            )
        flash("Update Successful")
        return redirect(url_for('guest_details', client_id=guest_id))

    return render_template("guest-details.html")


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
                    return get_users()
            else:
                # invalid password match
                flash("Incorrect Email and/or Password")
                return redirect(url_for("login"))

        else:
            # Email doesn't exist
            flash("Incorrect Email and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/guest-details/<client_id>")
def guest_details(client_id):
    guest = mongo.db.clients.find_one(
            {"_id": ObjectId(client_id)})
    bookings = list(mongo.db.bookings.find(
        {"client_id": client_id}))
    return render_template("guest-details.html", guest=guest, bookings=bookings)


@app.route("/users", methods=["GET", "POST"])
def get_users():

    account = mongo.db.users.find_one(
        {"email": session["email"]})["account"]

    admin = mongo.db.users.find_one(
        {"email": session["email"]}
    )["access"]
    if admin == "admin":
        admin = "true"
    else:
        admin = "false"

    users = list(mongo.db.users.find({
        "account": account
    }))

    return render_template("users.html", users=users, admin=admin)


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
        return get_users()
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
