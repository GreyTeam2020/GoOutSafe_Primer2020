from flask import Blueprint, render_template, redirect, request, session
from flask_login import current_user, login_user, logout_user, login_required

from monolith.database import db, User, Role, Restaurant
from monolith.forms import LoginForm

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email, password = form.data["email"], form.data["password"]
        q = db.session.query(User).filter(User.email == email)
        user = q.first()
        if user is not None and user.authenticate(password):
            login_user(user)
            q = db.session.query(Role).filter(Role.id == user.role_id)
            role = q.first()
<<<<<<< HEAD

            if role is not None:
                session["ROLE"] = role.value
                # if is operator, load restaurant information and load in session
                if role.value == 'OPERATOR':
                    q = db.session.query(Restaurant).filter(Restaurant.owner_id == user.id)
                    restaurant = q.first()
                    session["RESTAURANT_ID"] = restaurant.id
                    session["RESTAURANT_NAME"] = restaurant.name

=======
            session["ROLE"] = role.value
            # if is operator, load restaurant information and load in session
            if role.value == 'OPERATOR':
                q = db.session.query(Restaurant).filter(Restaurant.owner_id == user.id)
                restaurant = q.first()
                session["RESTAURANT_ID"] = restaurant.id
                session["RESTAURANT_NAME"] = restaurant.name
>>>>>>> 2abf67867e863be3e0d0cdb66acddd5403f231d5
            return redirect("/")
        else:
            return render_template("login.html", form=form, message="User not exist")
    return render_template("login.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    session.clear()  # remove all session objects, like role
    return redirect("/")
