"""
TODO
"""
import pytest
from monolith.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    ctx = app.app_context()
    ctx.push()

    with app.test_client() as client:
        yield client