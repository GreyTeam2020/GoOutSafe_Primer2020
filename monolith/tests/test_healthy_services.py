from datetime import datetime

import pytest

from monolith.database import db
from monolith.services import HealthyServices, User


@pytest.mark.usefixtures("client")
class Test_healthyServices:
    """"""

    def test_mark_positive(self):
        """

        :return:
        """
        user = db.session.query(User).filter_by(email="ham.burger@email.com").first()
        assert user is not None
        message = HealthyServices.mark_positive(user.email, user.phone)
        assert message != ""

    def test_mark_positive_already_covid(self):
        """
        :return:
        """
        user = db.session.query(User).filter_by(email="ham.burger@email.com").first()
        assert user is not None
        message = HealthyServices.mark_positive(user.email, user.phone)
        assert message != ""
        message = HealthyServices.mark_positive(user.email, user.phone)
        assert message == "User with email {} already Covid-19 positive".format(
            user.email
        )

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
        user = db.session.query(User).filter_by(email="ham.burger@email.com").first()
        assert user is not None
        message = HealthyServices.mark_positive(user.email, "")
        assert message != ""

    def test_mark_positive_user_by_email(self):
        """

        :return:
        """
        user = db.session.query(User).filter_by(email="ham.burger@email.com").first()
        assert user is not None
        message = HealthyServices.mark_positive("", user.phone)
        assert message != ""
