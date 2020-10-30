from flask import Blueprint, render_template, request

from monolith.auth import current_user
from monolith.database import (
    db,
    RestaurantTable,
    Reservation,
    Restaurant,
    OpeningHours,
    Positive,
)
import datetime

from flask_login import login_required


from monolith.services import BookingServices

book = Blueprint("book", __name__)


@book.route("/restaurant/book", methods=["GET", "POST"])
@login_required
def index():
    if current_user is not None and hasattr(current_user, "id"):
        # the date and time come as string, so I have to parse them and transform them in python datetime
        #
        py_datetime = datetime.datetime.strptime(
            request.form.get("reservation_date"), "%d/%m/%Y %H:%M"
        )
        #
        restaurant_id = int(request.form.get("restaurant_id"))
        #
        people_number = int(request.form.get("people_number"))
        #
        book = BookingServices.book(
            restaurant_id, current_user, py_datetime, people_number
        )

        if book[0] == False:
            return render_template("booking.html", success=False, error=book[1])
        else:
            return render_template(
                "booking.html",
                success=True,
                restaurant_name=book[1],
                table_name=book[2],
            )
    else:
        return render_template("booking.html", success=False, error="not logged in")
