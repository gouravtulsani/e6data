from flask import Flask
from e6blogs.config import Config
from e6blogs.models import db
from e6blogs import constants
from flasgger import Swagger


def create_app(db_uri='sqlite:///blogs.db'):
	app = Flask(__name__)
	Swagger(
		app,
		template=constants.SWAGGER_TEMPLATE
	)

	app.config.from_object(Config)
	app.config.update({
		"SQLALCHEMY_DATABASE_URI": db_uri
	})
	db.init_app(app)

	from e6blogs.apis.users import user_bp
	app.register_blueprint(user_bp)
	from e6blogs.apis.blogs import blog_bp
	app.register_blueprint(blog_bp)

	return app
