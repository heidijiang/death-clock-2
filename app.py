"""App runner."""
import pandas as pd
from flask import Flask, render_template, request, session

from views import death_clock as dc

app = Flask(__name__)
app.secret_key = "some secret key"

# two decorators, same function
@app.route("/")
@app.route("/index.html", methods=["POST"])
def index():
    """Index page."""
    return render_template("index.html", the_title="Death Clock")


@app.route("/name", methods=["POST"])
def name():
    """Query user."""
    username = request.form.get("name")
    session["name"] = username
    return render_template(
        "name.html",
        name=username,
    )


@app.route("/current_age", methods=["POST"])
def current_age():
    """Query age."""
    session["current_age"] = int(request.form.get("current_age"))
    return render_template(
        "current_age.html",
        current_age=session["current_age"],
    )


@app.route("/calculate", methods=["POST"])
def calculate():
    """Output."""
    data = pd.read_csv("assets/life_table_2015_processed.csv")
    death_generator = dc.DeathdayGenerator(
        name=session["name"],
        age=session["current_age"],
        data=data,
    )
    death_generator.get_death_date(data)
    return render_template(
        "calculate.html",
        name=death_generator.name,
        age=death_generator.age,
        death_date=death_generator.printed_date(),
        death_age=death_generator.death_age,
    )


if __name__ == "__main__":
    app.run(debug=True)
