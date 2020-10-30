import pytest
from monolith.database import db
from monolith.services import HealthyServices, User
from monolith.tests.utils import (
    create_user_on_db,
    del_user_on_db,
    positive_with_user_id,
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
        positive = positive_with_user_id(user.id)
        assert positive.marked is False

    def test_mark_positive_ok(self):
        """
        :return:
        """
        # an operator
        user = create_user_on_db()
        assert user is not None
        assert user.role_id is 3
        positive = positive_with_user_id(user.id, marked=True)
        assert positive is not None
        message = HealthyServices.mark_positive(user.email, user.phone)
        assert len(message) is 0
        db.session.query(User).filter_by(id=user.id).delete()
        db.session.commit()

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
        del_user_on_db(user.id)

    def test_mark_positive_user_by_email(self):
        """
        :return:
        """
        user = create_user_on_db()
        assert user is not None
        positive = positive_with_user_id(user.id)
        assert positive is None
        message = HealthyServices.mark_positive("", user.phone)
        assert len(message) is 0
        del_user_on_db(user.id)
