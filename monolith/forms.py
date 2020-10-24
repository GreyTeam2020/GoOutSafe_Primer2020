from flask_wtf import FlaskForm
import wtforms as f
from wtforms.validators import DataRequired, Length


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
    name_rest = f.StringField("name_rest", validators=[DataRequired()])
    password_rest = f.StringField("password_rest", validators=[DataRequired()])
    lat_rest = f.StringField("lat_rest", validators=[DataRequired()])
    lon_rest = f.StringField("lon_rest", validators=[DataRequired()])
    ## TODO(vincenzopalazzo) insert the real phone number lenght
    phone = f.StringField("phone_rest", validators=[DataRequired(), Length(min=5, max=25)])
    display = ["name_rest", "password_rest", "phone", "lat_rest", "lon_rest"]
