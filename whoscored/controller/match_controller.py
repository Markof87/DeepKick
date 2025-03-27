import logging
from flask import Blueprint, current_app

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from shared.container import Container
from whoscored.service.match_service import ScrapingService
from whoscored.dao.match_scraper_dao import MatchScraperDAO

from config import WHOSCORED_URL_BASE

match_blueprint = Blueprint('match', __name__)

whoscored_url = WHOSCORED_URL_BASE + 'matches/1874074/live/international-world-cup-qualification-uefa-2025-2026-england-latvia'

container = Container()
    
container.register('dao', MatchScraperDAO(whoscored_url))
container.register('service', ScrapingService(container.resolve('dao')))
    
service = container.resolve('service')


@match_blueprint.route('/match', methods=['GET'])
def get_match():
    cache = current_app.cache
    cached_data = cache.get('match_data')
    #logging.info('Cached data: %s', cached_data)
    if cached_data is not None:
        return cached_data

    match = service.get_match()
    cache.set('match_data', match, timeout=300)
    return match

@match_blueprint.route('/match/formations', methods=['GET'])
def get_match_formations():
    return get_match()["away"]["formations"]