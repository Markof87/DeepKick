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

@match_blueprint.route('/matchesbydate/<int:date>', methods=['GET'])
def get_all_matches_by_date(date):
    return service.get_all_matches_by_date(date)

@match_blueprint.route('/matches/<int:tournament_id>', methods=['GET'])
def get_all_matches_by_tournament(tournament_id):
    return service.get_all_matches_by_tournament(tournament_id)

@match_blueprint.route('/match/<int:match_id>', methods=['GET'])
def get_match_by_id(match_id):
    return service.get_match_by_id(match_id)

@match_blueprint.route('/match/<int:match_id>/team/<team>', methods=['GET'])
def get_match_formation(match_id, team):
    return service.get_match_formation(match_id, team)

@match_blueprint.route('/match/<int:match_id>/team/<int:team_id>/events', methods=['GET'])
def get_match_team_events(match_id, team_id):
    return service.get_match_team_events(match_id, team_id)

@match_blueprint.route('/match/<int:match_id>/team/<int:team_id>/events/count', methods=['GET'])
def get_match_team_events_count(match_id, team_id):
    return service.get_match_team_events_count(match_id, team_id)

@match_blueprint.route('/match/<int:match_id>/team/<int:team_id>/event/<event_name>', methods=['GET'])
def get_match_team_event_by_name(match_id, team_id, event_name):
    return service.get_match_team_event_by_name(match_id, team_id, event_name)

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

1. SavedShot  
2. CornerAwarded  
3. Pass  
4. Aerial  
5. MissedShots  
6. SubstitutionOff  
7. SubstitutionOn  
8. Foul  
9. BallRecovery  
10. Challenge  
11. Interception  
12. Clearance  
13. TakeOn  
14. End  
15. OffsideGiven  
16. Punch  
17. Tackle  
18. OffsideProvoked  
19. FormationSet

"""

@match_blueprint.route('/match/<int:match_id>/player/<int:player_id>/event/<event_name>', methods=['GET'])
def get_match_player_event_by_name(match_id, player_id, event_name):
    return service.get_match_player_event_by_name(match_id, player_id, event_name)

@match_blueprint.route('/match/<int:match_id>/player/<int:player_id>/event/<event_name>/count', methods=['POST'])
def image_report_creator(url, event_name, name, opponent):
    return service.image_report_creator(url, event_name, name, opponent)