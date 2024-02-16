import sqlite3
from flask import Blueprint, redirect, render_template, request, session, url_for

# Create a blueprint for the home routes
dashboard_page = Blueprint("dashboard", __name__)


def get_all_emp():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT firstName, lastName, EMP_ID, email, username FROM Users WHERE isAdmin=0"
    )
    users = cursor.fetchall()
    cursor.close()
    return users


def add_task(name, desc):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Assuming you have a table named 'tasks' with columns 'name', 'description', and 'member_username'
        cursor.execute(
            "INSERT INTO tasks (taskName, taskDesc) VALUES (?, ?)",
            (name, desc),
        )
    except Exception as e:
        print(e)

    finally:
        print("Tasks added")
        conn.commit()
        conn.close()


def get_tasks():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    return tasks


def get_all_teams():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teams")
    teams = cursor.fetchall()
    cursor.close()
    return teams


def create_new_team_name(team_name, team_desc):
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Assuming you have a table named 'tasks' with columns 'name', 'description', and 'member_username'
        cursor.execute(
            "INSERT INTO teams (teamName, teamDesc) VALUES (?, ?)",
            (team_name, team_desc),
        )
    except Exception as e:
        print(e)

    finally:
        print("Tasks added")
        conn.commit()
        conn.close()


def basic_round_robin(users, tasks):
    num_users = len(users)
    num_tasks = len(tasks)
    assignments = []

    # Iterate through each task and assign it to a user
    for i in range(num_tasks):
        user_index = i % num_users  # Get the index of the user to assign the task to
        user = users[user_index]
        task = tasks[i]
        print(user)
        print(task)
        assignment = (
            task[0],
            user[2],
        )  # Assuming the task and user data is stored in a tuple
        assignments.append(assignment)

    # Update the tasks table with the assigned usernames
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    for assignment in assignments:
        cursor.execute("UPDATE tasks SET UserName = ? WHERE taskName = ?", assignment)
    conn.commit()
    conn.close()

    return assignments


@dashboard_page.route("/dashboard/create_teams/assign_member", methods=["GET", "POST"])
def assign_team_member():
    teams = get_all_teams()
    print(teams)

    users = get_all_emp()
    print(users)
    if request.method == "POST":
        try:
            team_name = request.form["team_name"]
            team_member = request.form["team_member"]

            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            # Assuming you have a table named 'tasks' with columns 'name', 'description', and 'member_username'
            cursor.execute(
                "INSERT INTO teams (teamName, teamMembers) VALUES (?, ?)",
                (team_name, team_member),
            )
        except Exception as e:
            print(e)

        finally:
            print("Tasks added")
            conn.close()

    return render_template("/dashboard/create_teams.html", teams=teams, users=users)


# Define the route for the home page
@dashboard_page.route("/dashboard/home/", methods=["GET", "POST"])
def home():
    if session.get("logged_in"):
        username = session.get("username")

        # Fetch data from the database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Get the isAdmin value for the user
        cursor.execute("SELECT isAdmin FROM Users WHERE username=?", (username,))
        result = cursor.fetchone()
        is_admin = True if result[0] == 1 else False

        users = get_all_emp()
        # print(users)

        tasks = get_tasks()
        print(tasks)

        teams = get_all_teams()
        print(teams)

        conn.close()

        if request.method == "POST":
            task_name = request.form["task_name"]
            task_desc = request.form["task_desc"]

            result = add_task(task_name, task_desc)

        return render_template(
            "/dashboard/home.html",
            users=users,
            tasks=tasks,
            teams=teams,
            username=username,
            is_admin=is_admin,
        )
    else:
        # User is not logged in, redirect to login page
        return redirect(url_for("auth_page.signin"))


@dashboard_page.route("/dashboard/home", methods=["GET", "POST"])
def auto_assign_task():
    username = session.get("username")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Get the isAdmin value for the user
    cursor.execute("SELECT isAdmin FROM Users WHERE username=?", (username,))
    result = cursor.fetchone()
    is_admin = True if result[0] == 1 else False

    teams = get_all_teams()
    # print(teams)
    tasks = get_tasks()
    users = get_all_emp()

    if request.method == "POST":
        team_name = request.form["team_name"]

        cursor.execute("SELECT * FROM teams WHERE teamName = ?", (team_name,))
        users_list = cursor.fetchall()
        conn.close()

        # print(users_list)
        # print(tasks)

        result = basic_round_robin(users_list, tasks)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

    return render_template(
        "/dashboard/home.html",
        users=users,
        tasks=tasks,
        teams=teams,
        username=username,
        is_admin=is_admin,
    )


@dashboard_page.route("/dashboard/show_emp/")
def show_emp():
    # Fetch data from the database
    users = get_all_emp()
    # print(users)

    return render_template("/dashboard/show_emp.html", users=users)


@dashboard_page.route("/dashboard/create_teams/", methods=["GET", "POST"])
def create_team():
    teams = get_all_teams()
    print(teams)

    users = get_all_emp()
    print(users)

    if request.method == "POST":
        team_name = request.form["team_name"]
        team_desc = request.form["team_desc"]

        create_new_team_name(team_name, team_desc)

    return render_template("/dashboard/create_teams.html", teams=teams, users=users)
