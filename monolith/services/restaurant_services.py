from monolith.database import Restaurant, Menu, OpeningHours, RestaurantTable, Review
from monolith.forms import RestaurantForm
from monolith.database import db

from sqlalchemy.sql.expression import func

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
    def reviewRestaurant(restaurant_id, reviewer_id ,stars, review):
        '''
        This method insert a review to the specified restaurant
        '''
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
    def getThreeReviews(restaurant_id):
        '''
        Given the restaurant_di return three random reviews
        '''
        reviews = (db.session.query(Review)
        .filter_by(restaurant_id = restaurant_id)
        .order_by(func.random())
        .limit(3)
        .all())

        return reviews
    
    @staticmethod
    def getRestaurantName(restaurant_id):
        '''
        Given the id return the name of the resturant
        '''
        name = (db.session.query(Restaurant.name)
        .filter_by(id = restaurant_id)
        .first()
        )[0]

        return name