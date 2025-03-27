import logging
from flask import Blueprint, current_app, jsonify

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
    cache = current_app.cache
    cached_data = cache.get(f'match_data_{match_id}')
    #logging.info('Cached data: %s', cached_data)
    if cached_data is not None:
        return cached_data

    match = service.get_match_by_id(match_id)
    cache.set(f'match_data_{match_id}', match, timeout=86400)
    return match

@match_blueprint.route('/match/<int:match_id>/formations', methods=['GET'])
def get_match_formations_by_id(match_id):
    match_data = get_match_by_id(match_id)
    formations = {
        "home": match_data["home"]["formations"],
        "away": match_data["away"]["formations"]
    }
    return jsonify(formations)

@match_blueprint.route('/match/<int:match_id>/players', methods=['GET'])
def get_match_players_by_id(match_id):
    match_data = get_match_by_id(match_id)
    players = {
        "home": match_data["home"]["players"],
        "away": match_data["away"]["players"]
    }
    return jsonify(players)