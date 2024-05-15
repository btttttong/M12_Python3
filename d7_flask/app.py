from flask import Flask, render_template, redirect, url_for, request
import datetime


app = Flask(__name__)

bmis = []


def calculate_bmi(weight: float, height: float) -> float:
    return weight / (height**2)


# @app.route("/")
# def index():
#     return render_template("bmi.html")


@app.route("/", methods=["POST"])
def bmi():
    height = float(request.form.get("height"))
    weight = float(request.form.get("weight"))
    if height <= 0 or weight <= 0:
        return "Invalid input", 400
    bmi = calculate_bmi(weight, height)
    bmis.append(bmi)
    bmi_avg = sum(bmis) / len(bmis) if bmis else 0
    return render_template("bmi.html", bmi=bmi, bmi_avg=bmi_avg)


# @app.route("/index/<city>")
# def index(city):
#     return render_template("hello.html", city=city)


# @app.route("/about")
# def about():
#     return "this is about page"


# @app.route("/age/<int:birth_year>")
# def age(birth_year: int):
#     current_year = datetime.datetime.now().year
#     my_age = current_year - birth_year
#     if my_age < 18:
#         return redirect(url_for("legal_information"))

#     return f"Your age is {my_age}"


# @app.route("/legal")
# def legal_information():
#     return "You are under 18, you can't see this page"


# app.add_url_rule("/index", "index", index)
