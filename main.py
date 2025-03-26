import os
import logging
from flask import Flask
from taipy.gui import Gui
from routes import setup_routes

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Initialize Taipy
gui = Gui()

# Setup routes
setup_routes(app, gui)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
