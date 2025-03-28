import logging
from flask import Blueprint, jsonify

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from shared.container import Container
from whoscored.service.match_service import ScrapingService
from whoscored.dao.match_scraper_dao import MatchScraperDAO

match_blueprint = Blueprint('match', __name__)

container = Container()
container.register('dao', MatchScraperDAO())
container.register('service', ScrapingService(container.resolve('dao')))
    
service = container.resolve('service')

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
