import pytest
from app import create_app
from app.db import db
from app.config import TestConfig

@pytest.fixture
def client():
    app = create_app(TestConfig)
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()
