from flask import Flask
from flask_bootstrap import Bootstrap
from instance.db.sqlalchemyDB import db
from src.app import getSQLPath, getConfig


def InitApp():

    app = Flask(__name__)
    app.config.from_pyfile(getConfig())
    app.config["SQLALCHEMY_DATABASE_URI"] = getSQLPath()
    bootstrap = Bootstrap(app)
    db.init_app(app)

    return app
