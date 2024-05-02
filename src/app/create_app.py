from flask import Flask
from flask_bootstrap import Bootstrap
import os
from instance.db.db import db

cur_path = os.path.dirname(__file__)
src = os.path.abspath(os.path.join(cur_path, os.pardir))
parent = os.path.abspath(os.path.join(src, os.pardir))
config = os.path.join(parent, 'config', 'config.cfg')


def InitApp():

    app = Flask(__name__)
    app.config.from_pyfile(config)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{parent}/instance/app.db"
    bootstrap = Bootstrap(app)
    db.init_app(app)

    return app
