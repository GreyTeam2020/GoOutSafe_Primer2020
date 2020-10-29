from monolith.database import Restaurant, Menu, OpeningHours, RestaurantTable
from monolith.forms import RestaurantForm
from monolith.database import db


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