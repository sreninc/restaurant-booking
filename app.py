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
    clients = list(mongo.db.clients.find(
        {},
        {"first_name": 1, "last_name": 1}))

    for x in range(len(bookings)):
        for y in range(len(clients)): 
            if str(clients[y]["_id"]) == str(bookings[x]["client_id"]):
                bookings[x]["new_client_id"] = clients[y]["first_name"] + " " + clients[y]["last_name"]
    return render_template("bookings.html", bookings=bookings, clients=clients)


@app.route("/add_booking", methods=["GET", "POST"])
def add_booking():
    if request.method == "POST":
        # find the client
        client = mongo.db.clients.find_one({"_id": ObjectId(request.form.get("clientId"))})
        print(client)
        # create the client array to update with the new booking number
        client_array = {
            "first_name": client["first_name"],
            "last_name": client["last_name"],
            "email": client["email"],
            "mobile": client["mobile"],
            "marketing_consent": client["marketing_consent"],
            "bookings": client["bookings"] + 1,
            "created_by": client["created_by"]
        }
        # update the client
        mongo.db.clients.update({"_id": ObjectId(request.form.get("clientId"))}, client_array)
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


@app.route("/delete_booking/<booking_id>/<client_id>")
def delete_booking(booking_id, client_id):
    # find the client
    client = mongo.db.clients.find_one({"_id": ObjectId(client_id)})
    print(client)
    # create the client array to update with the new booking number
    client_array = {
        "first_name": client["first_name"],
        "last_name": client["last_name"],
        "email": client["email"],
        "mobile": client["mobile"],
        "marketing_consent": client["marketing_consent"],
        "bookings": client["bookings"] - 1,
        "created_by": client["created_by"]
    }
    # update the client
    mongo.db.clients.update({"_id": ObjectId(client_id)}, client_array)
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
            "first_name": request.form.get("firstName").capitalize(),
            "last_name": request.form.get("lastName").capitalize(),
            "email": request.form.get("email").lower(),
            "mobile": request.form.get("mobile"),
            "marketing_consent": marketing_consent,
            "bookings": 0,
            "created_by": session["email"]
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
