"""
TODO
"""
import pytest
import os
from monolith.app import create_app


@pytest.fixture
def client():
    # os.remove("{}/gooutsafe.db".format(os.path.dirname(os.path.realpath(__file__)).rsplit(os.sep, 2)[0]))
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    ctx = app.app_context()
    ctx.push()

    with app.test_client() as client:
        yield client
