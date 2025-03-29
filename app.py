import logging
from flask import Flask, send_from_directory
from flask_caching import Cache

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from whoscored.controller.match_controller import match_blueprint

logging.basicConfig(
    level=logging.DEBUG,  # Livello di logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s [%(levelname)s] %(message)s',  # Formato del messaggio
    handlers=[
        logging.FileHandler("app.log"),  # Salva i log in un file
        logging.StreamHandler()  # Mostra i log nella console
    ]
)

app = Flask(__name__)

app.config.from_pyfile('config.py')

cache = Cache(app)
app.cache = cache

app.register_blueprint(match_blueprint)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)