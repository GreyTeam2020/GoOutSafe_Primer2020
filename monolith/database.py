from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    password = db.Column(db.Unicode(128))
    dateofbirth = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_anonymous = False

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self._authenticated = False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def get_id(self):
        return self.id


class Restaurant(db.Model):
    __tablename__ = "restaurant"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text(100))

    likes = db.Column(
        db.Integer
    )  # will store the number of likes, periodically updated in background

    lat = db.Column(db.Float)  # restaurant latitude
    lon = db.Column(db.Float)  # restaurant longitude

    phone = db.Column(db.Integer)


class Like(db.Model):
    __tablename__ = "like"

    liker_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    liker = relationship("User", foreign_keys="Like.liker_id")

    restaurant_id = db.Column(
        db.Integer, db.ForeignKey("restaurant.id"), primary_key=True
    )
    restaurant = relationship("Restaurant", foreign_keys="Like.restaurant_id")

    marked = db.Column(
        db.Boolean, default=False
    )  # True iff it has been counted in Restaurant.likes
