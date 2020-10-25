from flask import Blueprint, redirect, render_template, request
from monolith.database import db, Restaurant, Like
from monolith.auth import admin_required, current_user
from flask_login import current_user, login_user, logout_user, login_required
from monolith.forms import RestaurantForm

restaurants = Blueprint("restaurants", __name__)


@restaurants.route("/restaurants")
def _restaurants(message=""):
    allrestaurants = db.session.query(Restaurant)
    return render_template(
        "restaurants.html",
        message=message,
        restaurants=allrestaurants,
        base_url="http://127.0.0.1:5000/restaurants",
    )


@restaurants.route("/restaurants/<restaurant_id>")
def restaurant_sheet(restaurant_id):
    record = db.session.query(Restaurant).filter_by(id=int(restaurant_id)).all()[0]
    return render_template(
        "restaurantsheet.html",
        name=record.name,
        likes=record.likes,
        lat=record.lat,
        lon=record.lon,
        phone=record.phone,
    )


@restaurants.route("/restaurants/like/<restaurant_id>")
@login_required
def _like(restaurant_id):
    q = Like.query.filter_by(liker_id=current_user.id, restaurant_id=restaurant_id)
    if q.first() != None:
        new_like = Like()
        new_like.liker_id = current_user.id
        new_like.restaurant_id = restaurant_id
        db.session.add(new_like)
        db.session.commit()
        message = ""
    else:
        message = "You've already liked this place!"
    return _restaurants(message)


@restaurants.route("/create_restaurant", methods=["GET", "POST"])
@login_required
def create_restaurant():
    form = RestaurantForm()
    if request.method == "POST":
        if form.validate_on_submit():
            new_restaurant = Restaurant()
            form.populate_obj(new_restaurant)
            db.session.add(new_restaurant)
            db.session.commit()
            return redirect("/")
    return render_template("create_restaurant.html", form=form)
