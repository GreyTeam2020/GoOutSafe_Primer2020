import os

import pytest
from monolith.database import db
from monolith.forms import UserForm
from monolith.services import HealthyServices, User, UserService
from monolith.tests.utils import create_user_on_db, del_user_on_db

from monolith.database import (
    Positive,
    User,
    OpeningHours,
    RestaurantTable,
    Reservation,
    Restaurant,
)

@pytest.mark.usefixtures("client")
class Test_healthyServices:
    """"""
    
    
    def test_mark_positive(self):
        """

        :return:
        """
        # an operator
        
        
        first_customer = User()
        first_customer.firstname = "John"
        first_customer.lastname = "Doe"
        first_customer.email = "test2@email.com"
        first_customer.phone = "65"
        first_customer.is_admin = False
        first_customer.set_password("customer")
        first_customer.role_id = 3
        db.session.add(first_customer)
        db.session.commit()
        

        q_already_positive = db.session.query(Positive)
            .filter(Positive.user_id==first_customer.id, Positive.marked==True)
            .first()
            

        assert q_already_positive is not None


    def test_mark_positive_user_not_exist(self):
        """
        :return:
        """
        message = HealthyServices.mark_positive(
            user_email="alibaba@alibaba.com", user_phone="1234555"
        )
        assert message == "The user is not registered"

    def test_mark_positive_nan_proprieties(self):
        """

        :return:
        """
        message = HealthyServices.mark_positive("", "")
        assert message == "Insert an email or a phone number"
   






















    