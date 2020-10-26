from flask import Blueprint, render_template, request

from monolith.auth import current_user
from monolith.database import db, RestaurantTable, Reservation, Restaurant
import datetime


book = Blueprint("book", __name__)


@book.route("/book", methods=["GET", "POST"])
def index():
    #return render_template("booking.html", success=False, error="not implemented yet")

    if current_user is not None and hasattr(current_user, "id"):
        # TODO: implement booking logic
        #request.form.get('date')
        # TODO: CHECK THE OPENING HOURS!!
        
        #the date and time come as string, so I have to parse them and transform them in python datetime
        py_datetime = datetime.datetime(int (request.form.get('date').split("/")[2].strip()), int (request.form.get('date').split("/")[1].strip()), int (request.form.get('date').split("/")[0].strip()), int (request.form.get('time').split(":")[0].strip()))
        
        #get the reservations in the same day, time and restaurant... drops reservation in table with max_seats < number of people requested
        reservations = db.session.query(RestaurantTable.id).join(Reservation, RestaurantTable.id == Reservation.table_id).filter(RestaurantTable.restaurant_id == request.form.get('restaurantID')).filter(Reservation.reservation_date == py_datetime).filter(RestaurantTable.max_seats >= int (request.form.get('people')))
        
        #from the list of all tables in the restaurant (the ones in which max_seats < number of people requested) drop the reserved ones
        all_restaurant_tables = db.session.query(RestaurantTable).filter(RestaurantTable.max_seats >= int (request.form.get('people'))).filter_by(restaurant_id = request.form.get('restaurantID')).filter(~RestaurantTable.id.in_(reservations)).all()
        
        #if there are tables available.. get the one with minimum max_seats
        if len (all_restaurant_tables) > 0:
            min_value = (all_restaurant_tables[0].id, all_restaurant_tables[0].max_seats)
            for i in range(1, len(all_restaurant_tables)):
                if (all_restaurant_tables[i].max_seats < min_value[1]):
                    min_value= (all_restaurant_tables[i].id, all_restaurant_tables[i].max_seats)
            
            restaurant_name = db.session.query(Restaurant.name).filter_by(id = request.form.get('restaurantID')).first()[0]
            table_name = db.session.query(RestaurantTable.name).filter_by(id = min_value[0]).first()[0]
            return render_template("booking.html", success=True, restaurant_name=restaurant_name, table_name=table_name)
        else:
            return render_template("booking.html", success=False, error="no tables available")
        
        return render_template("booking.html", success=True)
    else:
        return render_template("booking.html", success=False, error="not logged in")
