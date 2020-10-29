from flask import Blueprint, redirect, render_template, request, current_app, session
from monolith.database import db, User, Like, Role
from monolith.forms import UserForm
from monolith.utils import send_mail
from flask_login import login_user, current_user
from monolith.utils.dispaccer_events import DispatcherMessage
from monolith.app_constant import REGISTRATION_EMAIL
from monolith.services.user_service import UserService
from monolith.utils import send_mail
from monolith.auth import roles_allowed
from monolith.utils.formatter import my_date_formatter
from flask_login import current_user, login_user, login_required

users = Blueprint("users", __name__)


@users.route("/users")
def _users():
    users = db.session.query(User)
    return render_template("users.html", users=users)


@users.route("/user/create_operator", methods=["GET", "POST"])
def create_operator():
    form = UserForm()
    if request.method == "POST":
        if form.validate_on_submit():
            q = db.session.query(User).filter_by(email=form.email.data)
            if q.first() is not None:
                return render_template(
                    "create_user.html",
                    form=form,
                    message="Email {} already registered".format(form.email.data),
                )
            user = User()
            form.populate_obj(user)
            user = UserService.create_user(user, form.password.data, 2)
            if user is not None and user.authenticate(form.password.data):
                login_user(user)
            DispatcherMessage.send_message(
                type_message=REGISTRATION_EMAIL,
                params=[user.email, user.lastname, "112344"],
            )
            new_role = db.session.query(Role).filter_by(id=user.role_id).first()
            if new_role is not None:
                session["ROLE"] = new_role.value

            return redirect("/")
    return render_template("create_user.html", form=form)


@users.route("/user/create_user", methods=["GET", "POST"])
def create_user():
    form = UserForm()
    if request.method == "POST":
        if form.validate_on_submit():
            q = db.session.query(User).filter_by(email=form.email.data)
            if q.first() is not None:
                return render_template(
                    "create_user.html",
                    form=form,
                    message="Email {} already registered".format(form.email.data),
                )
            user = User()
            form.populate_obj(user)
            user = UserService.create_user(user, form.password.data)
            if user is not None and user.authenticate(form.password.data):
                login_user(user)
            DispatcherMessage.send_message(
                type_message=REGISTRATION_EMAIL,
                params=[user.email, user.lastname, "112344"],
            )
            new_role = db.session.query(Role).filter_by(id=user.role_id).first()
            if new_role is not None:
                session["ROLE"] = new_role.value

            return redirect("/")
    return render_template("create_user.html", form=form)


@users.route("/user/data", methods=["GET", "POST"])
@login_required
def user_data():
    message = None
    if request.method == "POST":
        # TODO: add logic to update data
        return redirect("/user/data")
    else:
        q = User.query.filter_by(id=current_user.id).first()
        if q is not None:
            form = UserForm(obj=q)
            return render_template(
                "user_data.html",
                form=form
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


@users.route("/customer/reservations")
@login_required
@roles_allowed(roles=["CUSTOMER"])
def myreservation():

    # for security reason, that are retrive on server side, not passed by params
    customer_id = current_user.id

    # filter params
    fromDate = request.args.get("fromDate", type=str)
    toDate = request.args.get("toDate", type=str)

    queryString = (
        "select reserv.id, reserv.reservation_date, reserv.people_number, tab.id as id_table, rest.name, rest.id as rest_id "
        "from reservation reserv "
        "join user cust on cust.id = reserv.customer_id "
        "join restaurant_table tab on reserv.table_id = tab.id "
        "join restaurant rest on rest.id = tab.restaurant_id "
        "where cust.id = :customer_id"
    )

    stmt = db.text(queryString)

    # bind filter params...
    params = {"customer_id": customer_id}
    if fromDate:
        params["fromDate"] = fromDate + " 00:00:00.000"
    if toDate:
        params["toDate"] = toDate + " 23:59:59.999"

    # execute and retrive results...
    result = db.engine.execute(stmt, params)
    reservations_as_list = result.fetchall()

    return render_template(
        "user_reservations.html",
        reservations_as_list=reservations_as_list,
        my_date_formatter=my_date_formatter,
    )


@users.route("/testsendemail")
def _testsendemail():
    # ------------------------
    testEmail = "PUTYOUREMAIL"  # PUT YOUR EMAIL FOR TEST and click to /login
    send_mail.send_possible_positive_contact(
        testEmail, "John Doe", "01/01/2020 21:30", "Il Paninaro"
    )
    send_mail.send_reservation_confirm(
        testEmail, "John Doe", "01/01/2020 21:30", "Il Paninaro", 10
    )
    send_mail.send_registration_confirm(
        testEmail, "John Doe", "qwertyuiopasdfghjklzxcvbnm"
    )
    send_mail.send_reservation_notification(
        testEmail, "John Doe", "Il Paninaro", "Richard Smith", "01/01/2020 21:30", 12, 8
    )
    # ------------------------
    return render_template("sendemailok.html", testEmail=testEmail)
