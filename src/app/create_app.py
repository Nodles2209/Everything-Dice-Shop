from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
from instance.db.sqlalchemyDB import db
from src.app import getSQLPath, getConfig


def InitApp():

    app = Flask(__name__)
    app.config.from_pyfile(getConfig())
    app.config["SQLALCHEMY_DATABASE_URI"] = getSQLPath()
    bootstrap = Bootstrap(app)
    csrf = CSRFProtect(app)
    db.init_app(app)

    return app
