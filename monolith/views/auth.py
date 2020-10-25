from flask import Blueprint, render_template, redirect, request, session
from flask_login import current_user, login_user, logout_user, login_required

from monolith.database import db, User, Role
from monolith.forms import LoginForm

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email, password = form.data["email"], form.data["password"]
        q = db.session.query(User).filter(User.email == email)
        user = q.first()
        print(q.first().id)
        if user is not None and user.authenticate(password):
            login_user(user)
            q = db.session.query(Role).filter(Role.id == user.role_id)
            role = q.first()
            session['ROLE'] = role.value
            return redirect("/")
    return render_template("login.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect("/")
