from flask import Flask
from flask_caching import Cache

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from whoscored.controller.match_controller import match_blueprint

app = Flask(__name__)

app.config.from_pyfile('config.py')

cache = Cache(app)
app.cache = cache

app.register_blueprint(match_blueprint)

if __name__ == '__main__':
    app.run(debug=True)