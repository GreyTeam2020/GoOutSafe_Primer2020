from datetime import datetime

from monolith.database import Restaurant, Menu, OpeningHours, RestaurantTable, Review, Reservation
from monolith.forms import RestaurantForm
from monolith.database import db

from sqlalchemy.sql.expression import func, extract


class RestaurantServices:
    """"""

    @staticmethod
    def create_new_restaurant(form: RestaurantForm, user_id: int, max_sit: int):
        """
        This method contains all logic save inside the a new restaurant
        :return:
        """
        restaurant = Restaurant()
        form.populate_obj(restaurant)
        restaurant.owner_id = user_id
        restaurant.likes = 0
        restaurant.covid_measures = form.covid_measures.data

        db.session.add(restaurant)
        db.session.commit()

        for i in range(int(form.n_tables.data)):
            new_table = RestaurantTable()
            new_table.restaurant_id = restaurant.id
            new_table.max_seats = max_sit
            new_table.available = True
            new_table.name = ""

            db.session.add(new_table)
            db.session.commit()

        # inserimento orari di apertura
        days = form.open_days.data
        for i in range(len(days)):
            new_opening = OpeningHours()
            new_opening.restaurant_id = restaurant.id
            new_opening.week_day = int(days[i])
            new_opening.open_lunch = form.open_lunch.data
            new_opening.close_lunch = form.close_lunch.data
            new_opening.open_dinner = form.open_dinner.data
            new_opening.close_dinner = form.close_dinner.data
            db.session.add(new_opening)
            db.session.commit()

        # inserimento tipi di cucina
        cuisin_type = form.cuisine.data
        for i in range(len(cuisin_type)):
            new_cuisine = Menu()
            new_cuisine.restaurant_id = restaurant.id
            new_cuisine.cusine = cuisin_type[i]
            new_cuisine.description = ""
            db.session.add(new_cuisine)
            db.session.commit()

        return restaurant

    @staticmethod
    def get_all_restaurants():
        """
        Method to return a list of all restaurants inside the database
        """
        all_restaurants = db.session.query(Restaurant).all()
        return all_restaurants

    @staticmethod
    def get_restaurants_id():
        """
        Method to return a list of all restaurants inside the database
        """
        all_restaurants = db.session.query(Restaurant).all()
        return all_restaurants

    @staticmethod
    def get_reservation_rest(owner_id, restaurant_id, from_date, to_date, email):
        """
        This method contains the logic to find all reservation in the restaurant
        with the filter on the date
        """

        queryString = (
            "select reserv.id, reserv.reservation_date, reserv.people_number, tab.id as id_table, cust.firstname, cust.lastname, cust.email, cust.phone from reservation reserv "
            "join user cust on cust.id = reserv.customer_id "
            "join restaurant_table tab on reserv.table_id = tab.id "
            "join restaurant rest on rest.id = tab.restaurant_id "
            "where rest.owner_id = :owner_id "
            "and rest.id = :restaurant_id "
        )

        # add filters...
        if from_date:
            queryString = queryString + " and  reserv.reservation_date > :fromDate"
        if to_date:
            queryString = queryString + " and  reserv.reservation_date < :toDate"
        if email:
            queryString = queryString + " and  cust.email = :email"
        queryString = queryString + " order by reserv.reservation_date desc"

        stmt = db.text(queryString)

        # bind filter params...
        params = {"owner_id": owner_id, "restaurant_id": restaurant_id}
        if from_date:
            params["fromDate"] = from_date + " 00:00:00.000"
        if to_date:
            params["toDate"] = to_date + " 23:59:59.999"
        if email:
            params["email"] = email

        # execute and retrive results...
        result = db.engine.execute(stmt, params)
        return result.fetchall()

    @staticmethod
    def review_restaurant(restaurant_id, reviewer_id, stars, review):
        """
        This method insert a review to the specified restaurant
        """
        if stars < 0 or stars > 5:
            return None

        new_review = Review()
        new_review.restaurant_id = restaurant_id
        new_review.reviewer_id = reviewer_id
        new_review.stars = stars
        new_review.review = review

        db.session.add(new_review)
        db.session.commit()

        return new_review

    @staticmethod
    def get_three_reviews(restaurant_id):
        """
        Given the restaurant_di return three random reviews
        """
        reviews = (
            db.session.query(Review)
            .filter_by(restaurant_id=restaurant_id)
            .order_by(func.random())
            .limit(3)
            .all()
        )

        return reviews

    @staticmethod
    def get_restaurant_name(restaurant_id):
        """
        Given the id return the name of the restaurant
        """
        name = db.session.query(Restaurant.name).filter_by(id=restaurant_id).first()[0]
        return name

    @staticmethod
    def get_restaurants_by_keyword(name: str = None):
        """
        This method contains the logic to perform the search restaurant by keywords
        The keywords supported are:
        :param name: is the name of restaurants
        """
        if name is None:
            raise Exception("Name is required to make this type of research")
        restaurants_list = db.session.query(Restaurant).filter_by(name=name).all()
        return restaurants_list

    @staticmethod
    def get_restaurant_people(restaurant_id: int):
        """
        Given the id of the restaurant return the number of people at lunch and dinner
        """
        openings = db.session.query(OpeningHours).filter(OpeningHours.week_day == datetime.today().weekday(),
                                                         OpeningHours.restaurant_id == restaurant_id).first()
        tables = db.session.query(RestaurantTable).filter_by(restaurant_id=restaurant_id).all()
        tables_id = []
        for table in tables:
            tables_id.append(table.id)

        reservations_l = db.session.query(Reservation).filter(
            Reservation.table_id.in_(tables_id),
            extract("day", Reservation.reservation_date) == extract("day", datetime.today()),
            extract("month", Reservation.reservation_date) == extract("month", datetime.today()),
            extract("year", Reservation.reservation_date) == extract("year", datetime.today()),
            extract("hour", Reservation.reservation_date) >= extract("hour", openings.open_lunch),
            extract("hour", Reservation.reservation_date) <= extract("hour", openings.close_lunch),
        ).all()

        reservations_d = db.session.query(Reservation).filter(
            Reservation.table_id.in_(tables_id),
            extract("day", Reservation.reservation_date) == extract("day", datetime.today()),
            extract("month", Reservation.reservation_date) == extract("month", datetime.today()),
            extract("year", Reservation.reservation_date) == extract("year", datetime.today()),
            extract("hour", Reservation.reservation_date) >= extract("hour", openings.open_dinner),
            extract("hour", Reservation.reservation_date) <= extract("hour", openings.close_dinner),
        ).all()

        return [len(reservations_l), len(reservations_d)]
