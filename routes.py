from flask import render_template, request, jsonify
from pages import teams

def setup_routes(app, gui):

    @app.route('/')
    def index():
        return render_template('index.html', content='')

    @app.route('/teams')
    def teams_page():
        return render_template('teams.html', content='')

