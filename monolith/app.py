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

        q = db.session.query(User).filter(User.email == "example@example.com")
        user = q.first()
        if user is None:
            example = User()
            example.firstname = "Admin"
            example.lastname = "Admin"
            example.email = "example@example.com"
            example.dateofbirth = datetime.datetime(2020, 10, 5)
            example.is_admin = True
            example.set_password("admin")
            example.role_id = 1
            db.session.add(example)
            db.session.commit()

        q = db.session.query(Restaurant).filter(Restaurant.id == 1)
        restaurant = q.first()
        if restaurant is None:
            example = Restaurant()
            example.name = "Trial Restaurant"
            example.likes = 42
            example.phone = 555123456
            example.lat = 43.720586
            example.lon = 10.408347
            db.session.add(example)
            db.session.commit()

        q = db.session.query(User).filter(User.email == "health_authority@gov.com")
        user = q.first()
        if user is None:
            health_authority = User()
            health_authority.firstname = "Health"
            health_authority.lastname = "Authority"
            health_authority.email = "health_authority@gov.com"
            health_authority.is_admin = False
            health_authority.set_password("nocovid")
            db.session.add(health_authority)
            db.session.commit()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")
