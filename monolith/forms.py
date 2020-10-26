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
    name = f.StringField("name", validators=[DataRequired()])
    ## FIXME(vincenzopalazzo) modify the phone length
    phone = f.StringField("phone", validators=[DataRequired(), Length(min=8, max=15)])
    lat = f.StringField("latitude", validators=[DataRequired()])
    lon = f.StringField("longitude", validators=[DataRequired()])
    n_tables = f.StringField("number of tables", validators=[DataRequired()])
    covid_m = f.StringField("Anti-Covid measures", validators=[DataRequired()])
    display = ["name", "phone", "lat", "lon", "n_tables", "covid_m"]
