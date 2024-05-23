import os
import pytest
from e6blogs import create_app, db


@pytest.fixture()
def app():
	app = create_app(db_uri='sqlite:///testing.db')

	with app.app_context():
		db.create_all()

	yield app


@pytest.fixture()
def client(app):  #passed by pytest
	return app.test_client()
