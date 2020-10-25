from flask import Blueprint, render_template

from monolith.auth import current_user


book = Blueprint("book", __name__)


@book.route("/book", methods=["GET", "POST"])
def index():
    return render_template("booking.html", success=False, error="not implemented yet")

    if current_user is not None and hasattr(current_user, "id"):
        # TODO: implement booking logic
        return render_template("booking.html", success=True)
    else:
        return render_template("booking.html", success=False, error="not logged in")
