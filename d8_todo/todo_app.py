from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import Form, StringField, PasswordField, validators, EmailField
from flask_wtf import FlaskForm
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "123456"
app.config["SESSION_LIFETIME"] = 600
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


def load_user_from_file():
    default_list = {
        "1": {"password": generate_password_hash("password"), "username": "BT"},
        "2": {"password": generate_password_hash("password"), "username": "user1"},
    }
    try:
        with open(app.instance_path + "/user_list.txt", "r") as file:
            user_from_file = json.load(file)
    except:
        user_from_file = default_list
    return user_from_file


users = load_user_from_file()


class User(UserMixin):
    def __init__(self, user_id, user_data):
        self.id = user_id
        self.username = user_data["username"]
        self.password = user_data["password"]


class UserRegistrationForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=4, max=25)])
    password = PasswordField("Password", [validators.Length(min=4, max=25)])
    cfpassword = PasswordField("Confirm Password", [validators.Length(min=4, max=25)])
    email = EmailField("Email", [validators.Length(min=6, max=35), validators.Email()])


@login_manager.user_loader
def get_user(user_id: str) -> User:
    user_data = users.get(user_id)
    if user_data:
        return User(user_id, user_data)
    return None


def load_todo_from_file():
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


todo_list = load_todo_from_file()
next_id = max([task["id"] for task in todo_list]) + 1 if todo_list else 1


def save_todo_to_file():
    with open(app.instance_path + "/todo_list.txt", "w") as file:
        json.dump(todo_list, file)


@app.route("/")
@login_required
def index():
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
                user_instance = User(user_id, user)
                login_user(user_instance)
                flash(f"You were logged in as {user['username']}")
                return redirect(url_for("index"))
        flash("Invalid credentials")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("login"))


@app.route("/add_task", methods=["GET", "POST"])
@login_required
def add_task():
    global next_id
    if request.method == "POST":
        new_task = request.form["task"]
        todo_list.append({"id": next_id, "task": new_task, "is_done": False})
        next_id += 1
        save_todo_to_file()
        return redirect(url_for("index"))
    return render_template("add_task.html")


@app.route("/delete_task/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    global todo_list
    task_name = [task["task"] for task in todo_list if task["id"] == task_id][0]
    todo_list = [task for task in todo_list if task["id"] != task_id]
    save_todo_to_file()
    flash(f"Task {task_name} deleted successfully")
    return redirect(url_for("index"))


@app.route("/mark_task_as_done/<int:task_id>", methods=["POST"])
@login_required
def mark_task_as_done(task_id):
    for task in todo_list:
        if task["id"] == task_id and not task["is_done"]:
            task["is_done"] = True
            flash(f"Task '{task['task']}' marked as done")
    save_todo_to_file()
    return redirect(url_for("index"))


@app.route("/edit_task/<int:task_id>", methods=["POST"])
@login_required
def edit_task(task_id):
    if request.method == "POST":
        new_task = request.form["task"]
        for task in todo_list:
            if task["id"] == task_id:
                task["task"] = new_task
                flash(f"Task '{task['task']}' updated successfully", category="info")
        save_todo_to_file()
        return redirect(url_for("index"))
    return render_template("index.html", todo_list=todo_list)


@app.route("/toggle_dark_mode", methods=["POST"])
@login_required
def toggle_dark_mode():
    dark_mode = request.form.get("dark_mode") == "true"
    session["dark_mode"] = dark_mode
    return "Dark mode preference saved", 200


@app.route("/register", methods=["GET", "POST"])
def register():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.cfpassword.data:
            flash("Passwords do not match")
            return render_template("register.html", form=form)
        user_id = str(len(users) + 1)
        username = form.username.data
        password = form.password.data
        users[user_id] = {
            "username": username,
            "password": generate_password_hash(password),
        }
        save_user()
        flash(f"User {username} registered successfully")
        return redirect(url_for("login"))
    else:
        flash(form.errors)
    return render_template("register.html", form=form)


def save_user():
    with open(app.instance_path + "/user_list.txt", "w") as file:
        json.dump(users, file)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
