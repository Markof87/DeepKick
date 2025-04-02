from flask import Blueprint

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from shared.container import Container
from whoscored.service.match_service import MatchScrapingService
from whoscored.dao.match_scraper_dao import MatchScraperDAO

match_blueprint = Blueprint('match', __name__)

container = Container()
container.register('dao', MatchScraperDAO())
container.register('service', MatchScrapingService(container.resolve('dao')))
    
service = container.resolve('service')

@match_blueprint.route('/tournaments', methods=['GET'])
def get_all_tournaments():
    return service.get_all_tournaments()

@match_blueprint.route('/matchestoday', methods=['GET'])
def get_all_matches_today():
    return service.get_all_matches_today()

@match_blueprint.route('/matches/<int:tournament_id>', methods=['GET'])
def get_all_matches_by_tournament(tournament_id):
    return service.get_all_matches_by_tournament(tournament_id)

@match_blueprint.route('/match/<int:match_id>', methods=['GET'])
def get_match_by_id(match_id):
    return service.get_match_by_id(match_id)

@match_blueprint.route('/match/<int:match_id>/formations', methods=['GET'])
def get_match_formations(match_id):
    return service.get_match_formations(match_id)

@match_blueprint.route('/match/<int:match_id>/players', methods=['GET'])
def get_match_players(match_id):
    return service.get_match_players(match_id)

@match_blueprint.route('/match/<int:match_id>/player/<int:player_id>', methods=['GET'])
def get_match_player_by_id(match_id, player_id):
    return service.get_match_player_by_id(match_id, player_id)

@match_blueprint.route('/match/<int:match_id>/player/<int:player_id>/events', methods=['GET'])
def get_match_player_events(match_id, player_id):
    return service.get_match_player_events(match_id, player_id)

"""
event_name può essere:

- Pass
- SavedShot
- MissedShots
- Tackle
- Challenge
- CornerAwarded
- BallRecovery
- OffsideGiven
- Foul
- Aerial

"""

@match_blueprint.route('/match/<int:match_id>/player/<int:player_id>/event/<event_name>', methods=['GET'])
def get_match_player_event_by_name(match_id, player_id, event_name):
    return service.get_match_player_event_by_name(match_id, player_id, event_name)
