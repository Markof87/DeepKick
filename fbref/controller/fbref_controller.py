from flask import Blueprint, request, redirect, url_for

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from shared.container import Container
from fbref.service.fbref_service import FBrefService

fbref_blueprint = Blueprint('datatable', __name__)

container = Container()
container.register('service', FBrefService())
    
service = container.resolve('service')

@fbref_blueprint.route('/teamseason_base_stats/tournament/<tournament>/season/<season>/type/<stat_type>', methods=['GET'])
def get_teamseason_base_stats(tournament, season, stat_type):
    return service.get_teamseason_base_stats(tournament, season, stat_type, False)

@fbref_blueprint.route('/teamseason_base_stats/tournament/<tournament>/season/<season>/type/<stat_type>/player', methods=['GET'])
def get_teamseason_base_stats_player(tournament, season, stat_type):
    return service.get_teamseason_base_stats(tournament, season, stat_type, True)

