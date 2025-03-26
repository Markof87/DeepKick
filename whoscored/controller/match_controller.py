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
def get_matches():
    cache = current_app.cache
    cached_data = cache.get('match_data')
    if cached_data is not None:
        return cached_data

    matches = service.get_match()
    cache.set('match_data', matches, timeout=300)
    return matches
