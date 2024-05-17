from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "123456"

# Users dictionary with nested dictionaries for user details
users = {
    "1": {"password": generate_password_hash("password"), "username": "BT"},
    "2": {"password": generate_password_hash("password"), "username": "user1"},
}


def load_from_file():
    default_list = [
        {"id": 1, "task": "develop todo webapplication", "is_done": False},
        {"id": 2, "task": 'Add "add new item" feature', "is_done": False},
        {"id": 3, "task": 'Add "delete item" button', "is_done": False},
        {"id": 4, "task": 'Add "mark task as done" button', "is_done": False},
    ]

    try:
        with open(app.instance_path + "/todo_list.txt", "r") as file:
            todo_from_file = json.load(file)
    except:
        todo_from_file = default_list

    for task in todo_from_file:
        if "is_done" not in task:
            task["is_done"] = False

    return todo_from_file


todo_list = load_from_file()
next_id = max([task["id"] for task in todo_list]) + 1 if todo_list else 1


def save_to_file():
    with open(app.instance_path + "/todo_list.txt", "w") as file:
        json.dump(todo_list, file)


@app.route("/")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html", todo_list=todo_list)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        for user_id, user in users.items():
            if username == user["username"] and check_password_hash(
                user["password"], password
            ):
                session["logged_in"] = True
                session["user_id"] = user_id
                flash(f"You were logged in as {user['username']}")
                return redirect(url_for("index"))
        flash("Invalid credentials")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("user_id", None)
    flash("You were logged out")
    return redirect(url_for("login"))


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    global next_id
    if request.method == "POST":
        new_task = request.form["task"]
        todo_list.append({"id": next_id, "task": new_task, "is_done": False})
        next_id += 1
        save_to_file()
        return redirect(url_for("index"))
    return render_template("add_task.html")


@app.route("/delete_task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    global todo_list
    task_name = [task["task"] for task in todo_list if task["id"] == task_id][0]
    todo_list = [task for task in todo_list if task["id"] != task_id]
    save_to_file()
    flash(f"Task {task_name} deleted successfully")
    return redirect(url_for("index"))


@app.route("/mark_task_as_done/<int:task_id>", methods=["POST"])
def mark_task_as_done(task_id):
    for task in todo_list:
        if task["id"] == task_id and not task["is_done"]:
            task["is_done"] = True
            flash(f"Task '{task['task']}' marked as done")
    save_to_file()
    return redirect(url_for("index"))


@app.route("/edit_task/<int:task_id>", methods=["POST"])
def edit_task(task_id):
    if request.method == "POST":
        new_task = request.form["task"]
        for task in todo_list:
            if task["id"] == task_id:
                task["task"] = new_task
                flash(f"Task '{task['task']}' updated successfully", category="info")
        save_to_file()
        return redirect(url_for("index"))
    return render_template("index.html", todo_list=todo_list)


@app.route("/toggle_dark_mode", methods=["POST"])
def toggle_dark_mode():
    dark_mode = request.form.get("dark_mode") == "true"
    session["dark_mode"] = dark_mode
    return "Dark mode preference saved", 200


if __name__ == "__main__":
    app.run(debug=True, port=5002)
