from flask import Flask
from flask_bootstrap import Bootstrap
import os

cur_path = os.path.dirname(__file__)
src = os.path.abspath(os.path.join(cur_path, os.pardir))
parent = os.path.abspath(os.path.join(src, os.pardir))
config = os.path.join(parent, 'config', 'config.cfg')

app = Flask(__name__)
app.config.from_pyfile(config)
bootstrap = Bootstrap(app)
