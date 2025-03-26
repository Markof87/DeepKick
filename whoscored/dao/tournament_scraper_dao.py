import re
import json
import pandas as pd
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.by import By

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from shared.utils import createEventsDF

from whoscored.dao.base_scraper_dao import BaseScraperDAO
import shared.scraper_service as ss

class TournamentScraperDAO(BaseScraperDAO):
    def __init__(self, url: str):
        self.url = url

    def fetch_data(self):
        #TODO: da valutare se portare fuori il driver
        driver = ss.constructWhoscoredWebDriver(self.url)

        n_tournaments = []

        button_all_tournaments = driver.find_element(By.ID, "All-Tournaments-btn")
        driver.execute_script("arguments[0].click();", button_all_tournaments)

        alphabeth_buttons = driver.find_elements(By.XPATH, f'//*[contains(@id, "index-")]')
        for alphabeth_button in alphabeth_buttons:
            driver.execute_script("arguments[0].click();", alphabeth_button)
            countries = driver.find_elements(By.XPATH, f'//*[contains(@id, "tournamentNavButton-")]')

            for country in countries:
                driver.execute_script("arguments[0].click();", country)
                display_element = country.find_element(By.XPATH, 'following-sibling::*')
                tournaments_found_list = display_element.find_elements(By.XPATH, './/div[contains(@class, "TournamentsDropdownMenu-module_allTournamentNavButtons__")]')
                country_name = country.get_attribute('innerText')
                for tournament_found in tournaments_found_list:
                    tournament_found_html = soup(tournament_found.get_attribute('innerHTML'), 'html.parser')
                    n_tournaments.append({
                        'country': country_name,
                        'href': tournament_found_html.find('a').get('href'),
                        'name': tournament_found_html.find('a').get_text()
                    })

        df_tournaments = pd.DataFrame(n_tournaments)

        driver.close()
        return df_tournaments
