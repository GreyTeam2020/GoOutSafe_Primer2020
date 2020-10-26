from flask import Blueprint, redirect, render_template, request, current_app
from monolith.database import db, Restaurant, Like, User
from flask_login import current_user, login_required
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
        id=restaurant_id,
        name=record.name,
        likes=record.likes,
        lat=record.lat,
        lon=record.lon,
        phone=record.phone,
        covid_measures=record.covid_measures,
    )


@restaurants.route("/restaurants/like/<restaurant_id>")
@login_required
def _like(restaurant_id):
    q = Like.query.filter_by(liker_id=current_user.id, restaurant_id=restaurant_id)
    if q.first() is not None:
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
            q = db.session.query(Restaurant).filter_by(
                name=form.name.data,
                phone=form.phone.data,
                lat=form.lat.data,
                lon=form.lon.data,
            )
            if q.first() is not None:
                return render_template(
                    "create_restaurant.html",
                    form=form,
                    message="Restaurant {} in {}:{} already existed".format(
                        form.name.data, form.lat.data, form.lon.data
                    ),
                )
            new_restaurant = Restaurant()
            q_user = db.session.query(User).filter_by(id=current_user.id).first()
            if q_user is None:
                return render_template("create_restaurant.html",
                                       form=form,
                                       message="User not logged")
            print(q_user)
            if q_user.role_id is 3:
                q_user.role_id = 2
                db.session.commit()
                current_app.logger.debug("User {} with id {} update from role {} to {}"
                                         .format(q_user.name, q_user.id, 3, q_user.role_id))
            form.populate_obj(new_restaurant)
            new_restaurant.likes = 0
            new_restaurant.covid_measures = "no information"
            db.session.add(new_restaurant)
            db.session.commit()
            return redirect("/")
    return render_template("create_restaurant.html", form=form)


@restaurants.route("/my_restaurant_data", methods=["GET", "POST"])
@login_required
def my_restaurant_data():
    form = RestaurantForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # TODO: implement logic
            # you should user error= if you want to display an error, for success instead use message=
            return render_template(
                "my_restaurant_data.html", form=form, error="not implemented yet"
            )
    return render_template("my_restaurant_data.html", form=form)


@restaurants.route("/my_restaurant_menu")
@login_required
def my_menu():
    # TODO: pass menu entries
    return render_template("my_menu.html")


@restaurants.route("/my_restaurant_photogallery")
@login_required
def my_photogallery():
    # TODO: pass menu entries
    return render_template("my_photogallery.html")


@restaurants.route("/my_reservations")
@login_required
def my_reservations():
    # TODO: pass reservations
    return render_template("my_reservations.html")
