import os

import pytest
from monolith.database import db
from monolith.forms import UserForm
from monolith.services import HealthyServices, User, UserService
from monolith.tests.utils import create_user_on_db, del_user_on_db


@pytest.mark.usefixtures("client")
class Test_healthyServices:
    """"""

    def test_mark_positive_ok(self):
        """

        :return:
        """
        # an operator
        user = create_user_on_db()
        assert user is not None
        assert user.role_id is 3
        message = HealthyServices.mark_positive(user.email, user.phone)
        assert message != ""
        db.session.query(User).filter_by(id=user.id).delete()
        db.session.commit()

    def test_mark_positive_already_covid(self):
        """
        :return:
        """
        user = create_user_on_db()
        assert user is not None
        assert user.role_id is 3
        message = HealthyServices.mark_positive(user.email, user.phone)
        assert message != ""
        message = HealthyServices.mark_positive(user.email, user.phone)
        assert message == "User with email {} already Covid-19 positive".format(
            user.email
        )
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
        message = HealthyServices.mark_positive(user.email, "")
        assert message != ""
        del_user_on_db(user.id)

    def test_mark_positive_user_by_email(self):
        """

        :return:
        """
        user = create_user_on_db()
        assert user is not None
        message = HealthyServices.mark_positive("", user.phone)
        assert message != ""
        del_user_on_db(user.id)
