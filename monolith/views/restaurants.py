from flask import Blueprint, redirect, render_template, request, session, current_app
from monolith.database import db, Restaurant, Like, Reservation, User
from monolith.auth import admin_required, current_user, roles_allowed
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
                                         .format(q_user.email, q_user.id, 3, q_user.role_id))
            form.populate_obj(new_restaurant)
            new_restaurant.likes = 0
            new_restaurant.covid_measures = "no information"
            db.session.add(new_restaurant)
            db.session.commit()
            return redirect("/")
    return render_template("create_restaurant.html", form=form)


@restaurants.route("/my_reservations")
@login_required
@roles_allowed(roles=["OPERATOR"])
def my_reservations():
    # http://localhost:5000/list_reservations?fromDate=2013-10-07&toDate=2014-10-07&email=john.doe@email.com

    # for security reason, that are retrive on server side, not passed by params
    owner_id = current_user.id
    restaurant_id = session["RESTAURANT_ID"]

    # filter params
    fromDate = request.args.get('fromDate', type=str)
    toDate = request.args.get('toDate', type=str)
    email = request.args.get('email', type=str)

    queryString = "select reserv.reservation_date, reserv.people_number, cust.firstname, cust.lastname, cust.email, tab.name as tabname from reservation reserv " \
        "join user cust on cust.id = reserv.customer_id " \
        "join restaurant_table tab on reserv.table_id = tab.id "  \
        "join restaurant rest on rest.id = tab.restaurant_id " \
        "where rest.owner_id = :owner_id " \
        "and rest.id = :restaurant_id "

    # add filters...
    if fromDate:
        queryString = queryString + " and  reserv.reservation_date > :fromDate"
    if toDate:
        queryString = queryString + " and  reserv.reservation_date < :toDate"
    if email:
        queryString = queryString + " and  cust.email = :email"
    queryString = queryString + " order by reserv.reservation_date desc"

    stmt = db.text(queryString)

    # bind filter params...
    params = {"owner_id": owner_id, "restaurant_id": restaurant_id}
    if fromDate:
        params["fromDate"] = fromDate + " 00:00:00.000"
    if toDate:
        params["toDate"] = toDate + " 23:59:59.999"
    if email:
        params["email"] = email

    # execute and retrive results...
    result = db.engine.execute(stmt, params)
    reservations_as_list = result.fetchall()

    return render_template(
        "list_reservations.html",
        reservations_as_list=reservations_as_list
    )
