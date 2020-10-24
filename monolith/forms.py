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
    """
    This class include the data that we want insert from the restaurant  from
    """
    name_rest = f.StringField("name restaurant", validators=[DataRequired()])
    lat_rest = f.StringField("latitude", validators=[DataRequired()])
    lon_rest = f.StringField("longitude", validators=[DataRequired()])
    phone = f.StringField("phone", validators=[DataRequired()])
    password_rest = f.PasswordField("password", validators=[DataRequired()])
    display = ["name_rest", "lat_rest", "lon_rest", "phone", "password_rest"]