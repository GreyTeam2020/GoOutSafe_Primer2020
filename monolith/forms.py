from flask_wtf import FlaskForm
import wtforms as f
from wtforms.validators import DataRequired, Length, Email, NumberRange


class LoginForm(FlaskForm):
    email = f.StringField("email", validators=[DataRequired()])
    password = f.PasswordField("password", validators=[DataRequired()])
    display = ["email", "password"]


class UserForm(FlaskForm):
    email = f.StringField("email", validators=[DataRequired(), Email()])
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
    n_tables = f.StringField(
        "Number of tables for 6 People", validators=[DataRequired()]
    )
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
            ("0", "Monday"),
            ("1", "Tuesday"),
            ("2", "Wednesday"),
            ("3", "Thursday"),
            ("4", "Friday"),
            ("5", "Saturday"),
            ("6", "Sunday"),
        ],
        validators=[DataRequired()],
    )
    open_lunch = f.TimeField("open time for lunch", validators=[DataRequired()])
    close_lunch = f.TimeField("close time for lunch", validators=[DataRequired()])
    open_dinner = f.TimeField("open time for dinner", validators=[DataRequired()])
    close_dinner = f.TimeField("close time for dinner", validators=[DataRequired()])
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


class RestaurantTableForm(FlaskForm):
    name = f.StringField("name", validators=[DataRequired()])
    capacity = f.IntegerField("capacity", validators=[DataRequired()])
    display = ["name", "capacity"]


class SearchUserForm(FlaskForm):
    email = f.StringField("email")
    phone = f.StringField("phone")
    display = ["email", "phone"]


class PhotoGalleryForm(FlaskForm):
    url = f.StringField("URL", validators=[DataRequired()])
    caption = f.StringField("caption")
    display = ["url", "caption"]

class ReviewForm(FlaskForm):
    stars = f.FloatField("stars", validators=[DataRequired()])
    review = f.StringField("review")
    display = ["stars", "review"]


class ReservationForm(FlaskForm):
    reservation_date = f.DateTimeField("Date", validators=[DataRequired()])
    people_number = f.IntegerField("N. of People", validators=[DataRequired()])
    restaurant_id = f.HiddenField("")
    display = ["reservation_date", "people_number", "restaurant_id"]
