import sys
import os

from flask import current_app, jsonify

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from whoscored.dao.match_scraper_dao import MatchScraperDAO
from shared.utils import image_creator
from shared.utils import find_player
from collections import Counter

class MatchScrapingService:
    def __init__(self, scraper_dao: MatchScraperDAO):
        self.scraper_dao = scraper_dao

    def get_all_tournaments(self):        
        all_tournaments = self.scraper_dao.fetch_top_tournaments()
        return all_tournaments

    def get_all_matches_by_date(self, date):
        cache = current_app.cache
        cached_data = cache.get(f'all_matches_by_date_{date}')
        if cached_data is not None:
            return cached_data
        
        all_matches = self.scraper_dao.fetch_date_matches(date)
        cache.set(f'all_matches_by_tournament_{date}', all_matches, timeout=86400)
        return all_matches
    
    def get_all_matches_by_tournament(self, tournament_id):
        cache = current_app.cache
        cached_data = cache.get(f'all_matches_by_tournament_{tournament_id}')
        if cached_data is not None:
            return cached_data
        
        all_matches_by_tournament = self.scraper_dao.fetch_data_matches_by_tournament(tournament_id)
        cache.set(f'all_matches_by_tournament_{tournament_id}', all_matches_by_tournament, timeout=86400)
        return all_matches_by_tournament

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
    
    def get_match_formation(self, match_id, team):
        match_data = self.get_match_by_id(match_id)
        formation_player_ids = match_data[team]["formations"][0]["playerIds"]
        players = match_data[team]["players"]

        # Map playerIds in formations to the corresponding player objects
        formation_players = [player for player in players if player["playerId"] in formation_player_ids]
        return formation_players

        # Extend the match_data with the mapped formation players
        match_data[team]["formations"][0]["players"] = formation_players
        return match_data
    
    def get_match_team_events(self, match_id, team_id):
        match_data = self.get_match_by_id(match_id)
        events = [event for event in match_data["events"] if event["teamId"]== team_id]
        return events
    
    def get_match_team_events_count(self, match_id, team_id):
        match_data = self.get_match_by_id(match_id)
        events = [event for event in match_data["events"] if event["teamId"]== team_id]
        event_counts = {event_name: {"count": count} for event_name, count in Counter(event["type"]["displayName"] for event in events).items()}
        return event_counts
        return events
    
    def get_match_team_event_by_name(self, match_id, team_id, event_name):
        match_data = self.get_match_team_events(match_id, team_id)
        events = [event for event in match_data if event["type"]["displayName"] == event_name]
        if events is None:
            return jsonify({"error": "Match events not found"}), 404
        
        return jsonify(events)
    
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
    
    def get_match_player_events(self, match_id, player_id):
        match_data = self.get_match_by_id(match_id)
        
        player_events = [event for event in match_data["events"] if event.get("playerId") == player_id]
        return player_events
    
    def get_match_player_event_by_name(self, match_id, player_id, event_name):
        match_data = self.get_match_by_id(match_id)
        
        player_events = [event for event in match_data["events"] if event.get("playerId") == player_id and event["type"]["displayName"] == event_name]
        if not player_events:
            return jsonify({"error": "Event not found"}), 404
        return player_events
    
    def image_report_creator(self, url, event_name, name, opponent):
        return image_creator(url, event_name, name, opponent)
    

