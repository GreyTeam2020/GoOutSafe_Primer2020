import pytest
from monolith.database import db
from monolith.services import HealthyServices, User
from monolith.tests.utils import (
    create_user_on_db,
    del_user_on_db,
    positive_with_user_id,
    delete_positive_with_user_id,
    delete_was_positive_with_user_id
)


@pytest.mark.usefixtures("client")
class Test_healthyServices:
    """"""

    def test_mark_positive_user_precondition(self):
        """
        :return:
        """
        # an operator
        user = create_user_on_db()
        assert user is not None
        assert user.role_id is 3
        positive = positive_with_user_id(user.id, marked=True)
        assert positive is None
        delete_positive_with_user_id(user.id)
        del_user_on_db(user.id)

    def test_mark_positive_ok(self):
        """
        :return:
        """
        # an operator
        user = create_user_on_db()
        assert user is not None
        assert user.role_id is 3
        positive = positive_with_user_id(user.id)
        assert positive is None
        message = HealthyServices.mark_positive(user.email, user.phone)
        assert len(message) is 0
        delete_positive_with_user_id(user.id)
        del_user_on_db(user.id)

    def test_mark_positive_already_covid(self):
        """
        :return:
        """
        user = create_user_on_db()
        assert user is not None
        assert user.role_id is 3
        positive = positive_with_user_id(user.id)
        assert positive is None
        message = HealthyServices.mark_positive(user.email, user.phone)
        assert len(message) is 0
        message = HealthyServices.mark_positive(user.email, user.phone)
        assert message == "User with email {} already Covid-19 positive".format(
            user.email
        )
        delete_positive_with_user_id(user.id)
        del_user_on_db(user.id)

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

    def test_mark_positive_user_by_email(self):
        """
        :return:
        """
        user = create_user_on_db()
        assert user is not None
        assert user.role_id is 3
        assert user is not None
        positive = positive_with_user_id(user.id)
        assert positive is None
        message = HealthyServices.mark_positive(user.email, "")
        assert len(message) is 0
        delete_positive_with_user_id(user.id)
        del_user_on_db(user.id)

    def test_mark_positive_user_by_phone(self):
        """
        :return:
        """
        user = create_user_on_db()
        assert user is not None
        positive = positive_with_user_id(user.id)
        assert positive is None
        message = HealthyServices.mark_positive("", user.phone)
        assert len(message) is 0
        delete_positive_with_user_id(user.id)
        del_user_on_db(user.id)

    def test_unmark_positive_ok(self):
        """
        :return:
        """
        user = create_user_on_db()
        assert user is not None
        assert user.role_id is 3
        positive = positive_with_user_id(user.id)
        assert positive is None
        message = HealthyServices.mark_positive(user.email, user.phone)
        assert len(message) is 0

        message = HealthyServices.unmark_positive(user.email, user.phone)
        assert len(message) is 0

        delete_was_positive_with_user_id(user.id)
        del_user_on_db(user.id)

    def test_unmark_user_not_positive(self):
        """
        :return:
        """
        user = create_user_on_db()
        assert user is not None
        assert user.role_id is 3

        message = HealthyServices.unmark_positive(user.email, user.phone)
        assert message == "User with email {} is not Covid-19 positive".format(
            user.email
        )
        
        delete_positive_with_user_id(user.id)
        del_user_on_db(user.id)


    def test_unmark_user_not_in_app(self):
        """
        :return:
        """
        message = HealthyServices.unmark_positive("alibaba@alibaba.com", "")
        assert message == "The user is not registered"

    
    def test_unmark_positive_nan_proprieties(self):
        """
        :return:
        """
        message = HealthyServices.mark_positive("", "")
        assert message == "Insert an email or a phone number"

    
    def test_unmark_positive_user_by_email(self):
        """
        :return:
        """
        user = create_user_on_db()
        assert user is not None
        assert user.role_id is 3
        positive = positive_with_user_id(user.id)
        assert positive is None
        message = HealthyServices.mark_positive(user.email, "")
        assert len(message) is 0

        message = HealthyServices.unmark_positive(user.email, "")
        assert len(message) is 0

        delete_was_positive_with_user_id(user.id)
        del_user_on_db(user.id)
    

    def test_mark_positive_user_by_phone(self):
        """
        :return:
        """
        user = create_user_on_db()
        assert user is not None
        assert user.role_id is 3
        positive = positive_with_user_id(user.id)
        assert positive is None
        message = HealthyServices.mark_positive("",user.phone)
        assert len(message) is 0

        message = HealthyServices.unmark_positive("",user.phone)
        assert len(message) is 0

        delete_was_positive_with_user_id(user.id)
        del_user_on_db(user.id)
    
