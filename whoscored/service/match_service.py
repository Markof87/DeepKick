import sys
import os

from flask import current_app, jsonify

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from whoscored.dao.match_scraper_dao import MatchScraperDAO
from shared.utils import find_player

class ScrapingService:
    def __init__(self, scraper_dao: MatchScraperDAO):
        self.scraper_dao = scraper_dao

    def get_match(self):
        return self.scraper_dao.fetch_data()
    
    def get_match_by_id(self, match_id):
        cache = current_app.cache
        cached_data = cache.get(f'match_data_{match_id}')
        if cached_data is not None:
            return cached_data
        
        match_data = self.scraper_dao.fetch_data(match_id)
        cache.set(f'match_data_{match_id}', match_data, timeout=86400)
        return match_data
    
    def get_match_formations(self, match_id):
        match_data = self.get_match_by_id(match_id)
        formations = {
            "home": match_data["home"]["formations"],
            "away": match_data["away"]["formations"]
        }
        return jsonify(formations)
    
    def get_match_players(self, match_id):
        match_data = self.get_match_by_id(match_id)
        players = {
            "home": match_data["home"]["players"],
            "away": match_data["away"]["players"]
        }
        return jsonify(players)
    
    def get_match_player_by_id(self, match_id, player_id):
        match_data = self.get_match_by_id(match_id)
        all_players = match_data["home"]["players"] + match_data["away"]["players"]
        player = find_player(all_players, player_id, "playerId")
        if player is None:
            return jsonify({"error": "Player not found"}), 404
        
        return jsonify(player)
    

