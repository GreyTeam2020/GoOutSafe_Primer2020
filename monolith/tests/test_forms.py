"""
TODO
"""

import pytest
from utils import login, logout


@pytest.mark.usefixtures("client")
def test_login_form_ok(client):
    response = login(client, "ham.burger@email.com", "operator")
    assert response.status_code == 200
    assert "Hi Ham" in response.data.decode("utf-8")

    ##TODO check if the user is login inside the DB
