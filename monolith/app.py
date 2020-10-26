from flask import Flask
from monolith.database import db, User, Restaurant, Role
from monolith.views import blueprints
from monolith.auth import login_manager
import datetime


def create_app():
    app = Flask(__name__)
    app.config["WTF_CSRF_SECRET_KEY"] = "A SECRET KEY"
    app.config["SECRET_KEY"] = "ANOTHER ONE"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gooutsafe.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    db.init_app(app)
    login_manager.init_app(app)
    db.create_all(app=app)

    # create a first admin user
    with app.app_context():

        # create the user roles
        q = db.session.query(Role).filter(Role.id == 1)
        role = q.first()
        if role is None:
            role = Role()
            role.value = "ADMIN"
            role.label = "Admin role"
            db.session.add(role)
            role = Role()
            role.value = "OPERATOR"
            role.label = "Operator role"
            db.session.add(role)
            role = Role()
            role.value = "CUSTOMER"
            role.label = "Customer role"
            db.session.add(role)
            role = Role()
            role.value = "HEALTH"
            role.label = "Health role"
            db.session.add(role)
            db.session.commit()

        # an Admin user
        q = db.session.query(User).filter(User.email == "admin@gooutsafe.com")
        user = q.first()
        if user is None:
            admin_user = User()
            admin_user.firstname = "Admin"
            admin_user.lastname = "Admin"
            admin_user.email = "admin@gooutsafe.com"
            admin_user.dateofbirth = datetime.datetime(2020, 10, 5)
            admin_user.is_admin = True
            admin_user.set_password("admin")
            admin_user.role_id = 1
            db.session.add(admin_user)
            db.session.commit()

        # an operator
        q = db.session.query(User).filter(User.email == "ham.burger@email.com")
        user = q.first()
        if user is None:
            first_customer = User()
            first_customer.firstname = "Ham"
            first_customer.lastname = "Burger"
            first_customer.email = "ham.burger@email.com"
            first_customer.is_admin = False
            first_customer.set_password("operator")
            first_customer.role_id = 2
            db.session.add(first_customer)
            db.session.commit()

        # a customer
        q = db.session.query(User).filter(User.email == "john.doe@email.com")
        user = q.first()
        if user is None:
            first_customer = User()
            first_customer.firstname = "John"
            first_customer.lastname = "Doe"
            first_customer.email = "john.doe@email.com"
            first_customer.is_admin = False
            first_customer.set_password("customer")
            first_customer.role_id = 3
            db.session.add(first_customer)
            db.session.commit()

        # health autority
        q = db.session.query(User).filter(User.email == "health_authority@gov.com")
        user = q.first()
        if user is None:
            health_authority = User()
            health_authority.firstname = "Health"
            health_authority.lastname = "Authority"
            health_authority.email = "health_authority@gov.com"
            health_authority.is_admin = False
            health_authority.set_password("nocovid")
            health_authority.role_id = 4
            db.session.add(health_authority)
            db.session.commit()

        # a restaurant
        q = db.session.query(Restaurant).filter(Restaurant.id == 1)
        restaurant = q.first()
        if restaurant is None:
            # load the first operator
            q = db.session.query(User).filter(User.email == "ham.burger@email.com")
            user = q.first()
            first_restaurant = Restaurant()
            first_restaurant.name = "Trial Restaurant"
            first_restaurant.likes = 42
            first_restaurant.phone = 555123456
            first_restaurant.covid_measures = "Distance between tables 2mt; Menù touch; Alcohol Gel; Only Electronic Payment"
            first_restaurant.lat = 43.720586
            first_restaurant.lon = 10.408347
            first_restaurant.owner_id = user.id
            db.session.add(first_restaurant)
            db.session.commit()
        # TODO: create some tables and reservation

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=True)
