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
    covid_measures = f.StringField("Anti-Covid measures", validators=[DataRequired()])
    # photo = f.FileField("Photo of restaurant")
    cuisine = f.SelectMultipleField(
        "Cuisine Type",
        choices=[
            ("Italian food", "Italian food"),
            ("Chinese food", "Chinese food"),
            ("Indian Food", "Indian Food"),
            ("Japanese Food", "Japanese Food"),
            ("Other", "Other"),
        ],
        validators=[DataRequired()],
    )
    open_days = f.SelectMultipleField(
        "Opening days",
        choices=[
            ("Monday", "Monday"),
            ("Tuesday", "Tuesday"),
            ("Wednesday", "Wednesday"),
            ("Thursday", "Thursday"),
            ("Friday", "Friday"),
            ("Saturday", "Saturday"),
            ("Sunday", "Sunday"),
        ],
        validators=[DataRequired()],
    )
    open_lunch = f.StringField("open time for lunch", validators=[DataRequired()])
    close_lunch = f.StringField("close time for lunch", validators=[DataRequired()])
    open_dinner = f.StringField("open time for dinner", validators=[DataRequired()])
    close_dinner = f.StringField("close time for dinner", validators=[DataRequired()])
    display = [
        "name",
        "phone",
        "lat",
        "lon",
        "n_tables",
        "cuisine",
        "open_days",
        "open_lunch",
        "close_lunch",
        "open_dinner",
        "close_dinner",
        "covid_measures",
    ]
