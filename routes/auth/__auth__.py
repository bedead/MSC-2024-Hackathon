import sqlite3
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
    session,
)

import time
import random

from routes.__config__ import Config

# Create a blueprint for the auth routes
auth_page_bp = Blueprint("auth_page", __name__)


def generate_emp_id():
    timestamp = int(time.time() * 1000)  # Get current timestamp in milliseconds
    random_num = random.randint(10000, 99999)  # Generate a random 5-digit number
    emp_id = str(timestamp)[-5:] + str(
        random_num
    )  # Combine the timestamp and random number
    return emp_id


@auth_page_bp.route("/auth/signup/")
def choose_signup():
    return render_template("/auth/choose.html")


@auth_page_bp.route("/auth/signup/member", methods=["GET", "POST"])
def signup_member():
    error_message = None
    if request.method == "POST":
        # Get user input from the registration form
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        emp_id = generate_emp_id()

        # Connect to the SQLite database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            # Execute a query to insert the user data into the database
            query = "INSERT INTO Users (firstName, lastName, username, email, password, EMP_ID, isAdmin) VALUES (?, ?, ?, ?, ?, ?, 0)"
            cursor.execute(
                query, (firstName, lastName, username, email, password, emp_id)
            )
            conn.commit()

            return redirect(url_for("auth_page.signin"))
        except Exception as e:
            print(f"Error has occured: ", e)
            error_message = e

    return render_template("/auth/signup_member.html", error_message=error_message)


@auth_page_bp.route("/auth/signup/lead", methods=["GET", "POST"])
def signup_lead():
    error_message = None
    if request.method == "POST":
        # Get user input from the registration form
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        admin = True

        # Connect to the SQLite database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            # Execute a query to insert the user data into the database
            query = "INSERT INTO Users (firstName, lastName, username, email, password, isAdmin) VALUES (?, ?, ?, ?, ?, 1)"
            cursor.execute(query, (firstName, lastName, username, email, password))
            conn.commit()

            return redirect(url_for("auth_page.signin"))
        except Exception as e:
            print(f"Error has occured: ", e)
            error_message = e

    return render_template("/auth/signup_lead.html", error_message=error_message)


@auth_page_bp.route("/auth/signin/", methods=["GET", "POST"])
def signin():
    error_message = None
    if request.method == "POST":
        # Perform user authentication
        username = request.form["username"]
        password = request.form["password"]

        # Connect to the SQLite database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Execute a query to check the username and password
        query = "SELECT * FROM Users WHERE UserName = ? AND Password = ?"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            # If authentication is successful, store user data in the session
            session["username"] = username  # Assuming UserName in first column
            session["logged_in"] = True
            conn.close()

            print(user[0])
            # print()

            return redirect(url_for("dashboard.home"))

        # Authentication failed, show error message
        error_message = "Invalid username or password"
        conn.close()

    return render_template("/auth/signin.html", error_message=error_message)


@auth_page_bp.route("/auth/logout/", methods=["GET", "POST"])
def logout():
    # print(session["email"])
    session.clear()
    return redirect(url_for("auth_page.signin"))
