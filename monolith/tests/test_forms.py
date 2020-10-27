"""
This test case covered all simple action that we can do from the UI
"""

import pytest
from utils import login, logout
from monolith.database import db, User


@pytest.mark.usefixtures("client")
def test_login_form_ok(client):
    """
    This test suit test the operation that we can do
    to login correctly an user
    """
    email = "ham.burger@email.com"
    password = "operator"
    response = login(client, email, password)
    assert response.status_code == 200
    assert "Hi Ham" in response.data.decode("utf-8")

    q = db.session.query(User).filter_by(email=email)
    q_user = q.first()
    assert q_user is not None
    assert q_user.authenticate(password) is True

    response = logout(client)
    assert response.status_code == 200
    assert "Hi" not in response.data.decode("utf-8")

    q = db.session.query(User).filter_by(email=email)
    q_user = q.first()
    assert q_user is not None


@pytest.mark.usefixtures("client")
def test_login_form_ko(client):
    """
        This test suit test the operation that we can do
        to login correctly an user
        """
    email = "vincenzopalazzo@email.com"
    password = "operator"
    response = login(client, email, password)
    assert response.status_code == 200
    assert "Hi" not in response.data.decode("utf-8")

    q = db.session.query(User).filter_by(email=email)
    q_user = q.first()
    assert q_user is None


@pytest.mark.usefixtures("client")
def test_register_new_user(client):
    pass


@pytest.mark.usefixtures("client")
def test_delete_user(client):
    pass

@pytest.mark.usefixtures("client")
def test_register_new_restaurant(client):
    pass

@pytest.mark.usefixtures("client")
def test_modify_new_restaurant(client):
    pass

@pytest.mark.usefixtures("client")
def test_research_restaurant_by_name(client):
    pass

@pytest.mark.usefixtures("client")
def test_send_communication_covid19(client):
    """
    This test case test the number of people that enter in contact with an people
    that have the covid19 in the same time of the restaurant visit
    """
    pass