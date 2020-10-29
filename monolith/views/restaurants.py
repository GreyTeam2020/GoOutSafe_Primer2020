from flask import Blueprint, redirect, render_template, request, session, current_app
from monolith.database import (
    db,
    Restaurant,
    Like,
    User,
    RestaurantTable,
    OpeningHours,
    Menu,
    PhotoGallery,
)
from monolith.forms import PhotoGalleryForm, ReviewForm
from monolith.services import RestaurantServices
from monolith.auth import roles_allowed
from flask_login import current_user, login_required
from monolith.forms import RestaurantForm, RestaurantTableForm
from monolith.utils.formatter import my_date_formatter

restaurants = Blueprint("restaurants", __name__)

_max_seats = 6


@restaurants.route("/restaurant/restaurants")
def _restaurants(message="", _test=""):
    """
    Return the list of restaurants stored inside the db
    """
    allrestaurants = RestaurantServices.get_all_restaurants()
    if len(_test) == 0:
        _test = "all_rest_test"
    return render_template(
        "restaurants.html",
        message=message,
        _test=_test,
        restaurants=allrestaurants,
        base_url="http://127.0.0.1:5000/restaurants",
    )


@restaurants.route("/restaurant/<restaurant_id>")
def restaurant_sheet(restaurant_id):
    """
    Missing refactoring to services
    :param restaurant_id:
    :return:
    """
    record = db.session.query(Restaurant).filter_by(id=int(restaurant_id)).all()[0]
    weekDaysLabel = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    q_hours = (
        db.session.query(OpeningHours).filter_by(restaurant_id=int(restaurant_id)).all()
    )
    q_cuisine = db.session.query(Menu).filter_by(restaurant_id=int(restaurant_id)).all()
    photos = PhotoGallery.query.filter_by(restaurant_id=int(restaurant_id)).all()
    ## FIXME(vincenzopalazzo): This is only a test to try to fix
    session["RESTAURANT_ID"] = restaurant_id

    review_form = ReviewForm()

    return render_template(
        "restaurantsheet.html",
        id=restaurant_id,
        name=record.name,
        likes=record.likes,
        lat=record.lat,
        lon=record.lon,
        phone=record.phone,
        covid_measures=record.covid_measures,
        hours=q_hours,
        cuisine=q_cuisine,
        weekDaysLabel=weekDaysLabel,
        photos=photos,
        review_form=review_form,
        _test="visit_rest_test",
    )


@restaurants.route("/restaurant/like/<restaurant_id>")
@login_required
def _like(restaurant_id):
    """
    TODO user restaurant services
    """
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


@restaurants.route("/restaurant/create", methods=["GET", "POST"])
@login_required
@roles_allowed(roles=["OPERATOR"])
def create_restaurant():
    """
    TODO user restaurant services
    """
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
            q_user = db.session.query(User).filter_by(id=current_user.id).first()
            if q_user is None:
                return render_template(
                    "create_restaurant.html", form=form, message="User not logged"
                )

            # set the owner
            RestaurantServices.create_new_restaurant(form, q_user.id, _max_seats)
            ##new_restaurant = Restaurant()

            ##TODO remove this code here
            """
            if q_user.role_id is not 2:
                q_user.role_id = 2
                db.session.commit()
                current_app.logger.debug(
                    "User {} with id {} update from role {} to {}".format(
                        q_user.email, q_user.id, 3, q_user.role_id
                    )
                )
            """
            # set the new role in session
            # if not the role will be anonymous
            session["ROLE"] = "OPERATOR"

            return redirect("/")
    return render_template("create_restaurant.html", form=form)


@restaurants.route("/restaurant/reservations")
@login_required
@roles_allowed(roles=["OPERATOR"])
def my_reservations():
    # http://localhost:5000/my_reservations?fromDate=2013-10-07&toDate=2014-10-07&email=john.doe@email.com

    # for security reason, that are retrive on server side, not passed by params
    owner_id = current_user.id
    restaurant_id = session["RESTAURANT_ID"]

    # filter params
    fromDate = request.args.get("fromDate", type=str)
    toDate = request.args.get("toDate", type=str)
    email = request.args.get("email", type=str)

    reservations_as_list = RestaurantServices.get_reservation_rest(
        owner_id, restaurant_id, fromDate, toDate, email
    )

    return render_template(
        "reservations.html",
        _test="restaurant_reservations_test",
        reservations_as_list=reservations_as_list,
        my_date_formatter=my_date_formatter,
    )


@restaurants.route("/restaurant/data", methods=["GET", "POST"])
@login_required
@roles_allowed(roles=["OPERATOR"])
def my_data():
    message = None
    if request.method == "POST":
        # TODO: add logic to update data
        return redirect("/restaurant/my_restaurant_data")
    else:
        q = Restaurant.query.filter_by(id=session["RESTAURANT_ID"]).first()
        if q is not None:
            print(q.covid_measures)
            form = RestaurantForm(obj=q)
            form2 = RestaurantTableForm()
            tables = RestaurantTable.query.filter_by(
                restaurant_id=session["RESTAURANT_ID"]
            )
            return render_template(
                "restaurant_data.html",
                form=form,
                only=["name", "lat", "lon", "covid_measures"],
                tables=tables,
                form2=form2,
            )
        else:
            return redirect("/restaurant/create_restaurant")

    # get the resturant info and fill the form
    # this part is both for POST and GET requests
    q = Restaurant.query.filter_by(id=session["RESTAURANT_ID"]).first()
    if q is not None:
        print(q.covid_measures)
        form = RestaurantForm(obj=q)
        form2 = RestaurantTableForm()
        tables = RestaurantTable.query.filter_by(restaurant_id=session["RESTAURANT_ID"])
        return render_template(
            "restaurant_data.html",
            form=form,
            only=["name", "lat", "lon", "covid_measures"],
            tables=tables,
            form2=form2,
            message=message,
        )
    else:
        return redirect("/restaurant/create_restaurant")


@restaurants.route("/restaurant/tables", methods=["GET", "POST"])
@login_required
@roles_allowed(roles=["OPERATOR"])
def my_tables():
    if request.method == "POST":
        # insert the table with data provided by the form
        table = RestaurantTable()
        table.restaurant_id = session["RESTAURANT_ID"]
        table.max_seats = request.form.get("capacity")
        table.name = request.form.get("name")
        db.session.add(table)
        db.session.commit()
        ##
        return redirect("/restaurant/data")

    elif request.method == "GET":
        # delete the table specified by the get request
        RestaurantTable.query.filter_by(id=request.args.get("id")).delete()
        db.session.commit()
        return redirect("/restaurant/data")


@restaurants.route("/restaurant/photogallery", methods=["GET", "POST"])
@login_required
@roles_allowed(roles=["OPERATOR"])
def my_photogallery():
    if request.method == "POST":
        form = PhotoGalleryForm()
        # add photo to the db
        if form.validate_on_submit():
            photo_gallery = PhotoGallery()
            photo_gallery.caption = form.data["caption"]
            photo_gallery.url = form.data["url"]
            photo_gallery.restaurant_id = session["RESTAURANT_ID"]
            db.session.add(photo_gallery)
            db.session.commit()

        return redirect("/restaurant/photogallery")
    else:
        photos = PhotoGallery.query.filter_by(
            restaurant_id=session["RESTAURANT_ID"]
        ).all()
        form = PhotoGalleryForm()
        return render_template("photogallery.html", form=form, photos=photos)


@restaurants.route("/restaurant/review/<restaurant_id>", methods=["GET", "POST"])
@login_required
@roles_allowed(roles=["OPERATOR", "CUSTOMER"])
def restaurantReview(restaurant_id):
    if request.method == "POST":
        form = ReviewForm()
        if (
            RestaurantServices.reviewRestaurant(
                restaurant_id, current_user.id, form.data["stars"], form.data["review"]
            )
            is not None
        ):
            print("Review inserted!")
            return redirect("/")

    return redirect("/")
