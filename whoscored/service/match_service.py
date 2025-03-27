import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from whoscored.dao.match_scraper_dao import MatchScraperDAO

class ScrapingService:
    def __init__(self, scraper_dao: MatchScraperDAO):
        self.scraper_dao = scraper_dao

    def get_match(self):
        return self.scraper_dao.fetch_data()
    
    def get_match_by_id(self, match_id):
        return self.scraper_dao.fetch_data(match_id)
    

