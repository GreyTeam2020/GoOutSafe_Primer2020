from flask_wtf import FlaskForm
import wtforms as f
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = f.StringField("email", validators=[DataRequired()])
    password = f.PasswordField("password", validators=[DataRequired()])
    display = ["email", "password"]


class UserForm(FlaskForm):
    email = f.StringField("email", validators=[DataRequired()])
    firstname = f.StringField("firstname", validators=[DataRequired()])
    lastname = f.StringField("lastname", validators=[DataRequired()])
    password = f.PasswordField("password", validators=[DataRequired()])
    dateofbirth = f.DateField("dateofbirth", format="%d/%m/%Y")
    display = ["email", "firstname", "lastname", "password", "dateofbirth"]


class RestaurantForm(FlaskForm):
    name = f.StringField("name", validators=[DataRequired()])
    phone = f.StringField("phone", validators=[DataRequired()])
    lat = f.StringField("latitude", validators=[DataRequired()])
    lon = f.StringField("longitude", validators=[DataRequired()])
    display = ["name", "phone", "lat", "lon"]
