from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    current_app,
    abort,
)
from monolith.database import (
    db,
    Restaurant,
    User,
    RestaurantTable,
    OpeningHours,
    Menu,
    PhotoGallery,
    MenuDish,
)
from monolith.forms import PhotoGalleryForm, ReviewForm, ReservationForm, DishForm
from monolith.services import RestaurantServices
from monolith.auth import roles_allowed
from flask_login import current_user, login_required
from monolith.forms import RestaurantForm, RestaurantTableForm
from monolith.utils.formatter import my_date_formatter

restaurants = Blueprint("restaurants", __name__)

_max_seats = 6


@restaurants.route("/restaurant/<restaurant_id>")
def restaurant_sheet(restaurant_id):
    """
    Missing refactoring to services
    :param restaurant_id:
    """
    weekDaysLabel = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    # record = db.session.query(Restaurant).filter_by(id=int(restaurant_id)).all()
    # if record is not None:
    #    record = record[0]

    model = RestaurantServices.get_all_restaurants_info(restaurant_id)
    if model is None:
        abort(501)

    # q_hours = db.session.query(OpeningHours).filter_by(restaurant_id=int(restaurant_id)).all()
    # q_cuisine = db.session.query(Menu).filter_by(restaurant_id=int(restaurant_id)).all()
    # photos = PhotoGallery.query.filter_by(restaurant_id=int(restaurant_id)).all()
    # dishes = db.session.query(MenuDish).filter_by(restaurant_id=restaurant_id).all()

    review_form = ReviewForm()
    book_form = ReservationForm()

    return render_template(
        "restaurantsheet.html",
        weekDaysLabel=weekDaysLabel,
        id=restaurant_id,
        name=model.name,
        lat=model.lat,
        lon=model.lon,
        phone=model.phone,
        covid_measures=model.covid_measures,
        hours=model.opening_hours,
        cuisine=model.covid_measures,
        photos=model.photos,
        dishes=model.dishes,
        review_form=review_form,
        book_form=book_form,
        reviews=RestaurantServices.get_three_reviews(restaurant_id),
        _test="visit_rest_test",
    )


@restaurants.route("/restaurant/create", methods=["GET", "POST"])
@login_required
@roles_allowed(roles=["OPERATOR"])
def create_restaurant():
    """
    This flask method give the possibility with a POST request to create a new
    restaurant inside the system
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
                    _test="rest_already_here_test",
                    message="Restaurant {} in {}:{} already existed".format(
                        form.name.data, form.lat.data, form.lon.data
                    ),
                )
            q_user = db.session.query(User).filter_by(id=current_user.id).first()
            if q_user is None:
                return render_template(
                    "create_restaurant.html",
                    _test="anonymus_user_test",
                    form=form,
                    message="User not logged",
                )

            # set the owner
            newrestaurant = RestaurantServices.create_new_restaurant(
                form, q_user.id, _max_seats
            )
            session["RESTAURANT_ID"] = newrestaurant.id
            return redirect("/")
    return render_template(
        "create_restaurant.html", _test="create_rest_test", form=form
    )


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
        reservations_n=RestaurantServices.get_restaurant_people(restaurant_id),
    )


@restaurants.route("/restaurant/data", methods=["GET", "POST"])
@login_required
@roles_allowed(roles=["OPERATOR"])
def my_data():
    """
    TODO(vincenzopalazzo) add information
    This API call give the possibility to the user TODO
    """
    message = None
    if request.method == "POST":
        # update query
        q = Restaurant.query.filter_by(id=session["RESTAURANT_ID"]).update(
            {
                "name": request.form.get("name"),
                "lat": request.form.get("lat"),
                "lon": request.form.get("lon"),
                "covid_measures": request.form.get("covid_measures"),
            }
        )
        # if no resturant match the update query (session problem probably)
        if q == 0:
            message = "Some Errors occurs"
        else:
            db.session.commit()
            message = "Restaurant data has been modified."

    # get the resturant info and fill the form
    # this part is both for POST and GET requests
    q = Restaurant.query.filter_by(id=session["RESTAURANT_ID"]).first()
    if q is not None:
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
        return redirect("/create_restaurant")


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


@restaurants.route("/restaurant/menu", methods=["GET", "POST"])
@login_required
@roles_allowed(roles=["OPERATOR"])
def my_menu():
    if request.method == "POST":
        form = DishForm()
        # add dish to the db
        if form.validate_on_submit():
            dish = MenuDish()
            dish.name = form.data["name"]
            dish.price = form.data["price"]
            dish.restaurant_id = session["RESTAURANT_ID"]
            db.session.add(dish)
            db.session.commit()
            _test = "menu_ok_test"
        else:
            _test = "menu_ko_form_test"
            print(form.errors)
        return render_template(
            "restaurant_menu.html", _test=_test, form=form, dishes=[]
        )
    else:
        dishes = MenuDish.query.filter_by(restaurant_id=session["RESTAURANT_ID"]).all()
        form = DishForm()
        return render_template(
            "restaurant_menu.html", _test="menu_view_test", form=form, dishes=dishes
        )


@restaurants.route("/restaurant/menu/delete/<dish_id>")
@login_required
@roles_allowed(roles=["OPERATOR"])
def delete_dish(dish_id):
    db.session.query(MenuDish).filter_by(id=dish_id).delete()
    db.session.commit()
    return redirect("/restaurant/menu")


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
@roles_allowed(roles=["CUSTOMER"])
def restaurant_review(restaurant_id):
    if request.method == "POST":
        form = ReviewForm()
        review = RestaurantServices.review_restaurant(
            restaurant_id, current_user.id, form.data["stars"], form.data["review"]
        )
        if review is not None:
            print("Review inserted!")
            return render_template(
                "review.html",
                _test="review_done_test",
                restaurant_name=RestaurantServices.get_restaurant_name(restaurant_id),
                review=review,
            )

    return render_template(
        "review.html",
        _test="review_done_test",
        error="An error occur inserting the review. Try again later.",
    )


@restaurants.route("/restaurant/search/<name_rest>", methods=["GET"])
def search_restaurant(name_rest):
    current_app.logger.debug(
        "An user want search a restaurant with name {}".format(name_rest)
    )

    file = "index.html"
    if "ROLE" in session and session["ROLE"] == "CUSTOMER":
        file = "index_customer.html"

    form = ReservationForm()
    filter_by_name = RestaurantServices.get_restaurants_by_keyword(name=name_rest)
    return render_template(
        file,
        _test="rest_search_test",
        restaurants=filter_by_name,
        search=name_rest,
        form=form,
    )


@restaurants.route("/restaurant/checkinreservations/<reservation_id>")
@login_required
@roles_allowed(roles=["OPERATOR"])
def checkin_reservations(reservation_id):
    RestaurantServices.checkin_reservations(reservation_id)
    return redirect("/restaurant/reservations")
