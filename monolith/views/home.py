from flask import Blueprint, render_template

from monolith.database import db, Restaurant

home = Blueprint("home", __name__)

@home.route("/")
def index():
    restaurants = db.session.query(Restaurant)

    return render_template("index.html", restaurants=restaurants)
