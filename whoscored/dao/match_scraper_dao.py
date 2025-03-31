import re
import json
from selenium.webdriver.common.by import By

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from shared.utils import createEventsDF, fetch_top_tournaments

from config import WHOSCORED_URL_BASE

from whoscored.dao.base_scraper_dao import BaseScraperDAO
import shared.scraper_service as ss

class MatchScraperDAO(BaseScraperDAO):

    def fetch_data(self, match_id):
        driver = ss.constructWhoscoredWebDriver(WHOSCORED_URL_BASE + 'matches/' + str(match_id) + '/live')
        # get script data from page source
        script_content = driver.find_element(By.XPATH, '//*[@id="layout-wrapper"]/script[1]').get_attribute('innerHTML')

        # clean script content
        script_content = re.sub(r"[\n\t]*", "", script_content)
        script_content = script_content[script_content.index("matchId"):script_content.rindex("}")]

        # this will give script content in list form 
        script_content_list = list(filter(None, script_content.strip().split(',            ')))
        metadata = script_content_list.pop(1) 

        # string format to json format
        match_data = json.loads(metadata[metadata.index('{'):])
        keys = [item[:item.index(':')].strip() for item in script_content_list]
        values = [item[item.index(':')+1:].strip() for item in script_content_list]
        for key,val in zip(keys, values):
            match_data[key] = json.loads(val)

        # get other details about the match
        region = driver.find_element(By.XPATH, '//*[@id="breadcrumb-nav"]/span[1]').text
        league = driver.find_element(By.XPATH, '//*[@id="breadcrumb-nav"]/a').text.split(' - ')[0]
        season = driver.find_element(By.XPATH, '//*[@id="breadcrumb-nav"]/a').text.split(' - ')[1]
        if len(driver.find_element(By.XPATH, '//*[@id="breadcrumb-nav"]/a').text.split(' - ')) == 2:
            competition_type = 'League'
            competition_stage = ''
        elif len(driver.find_element(By.XPATH, '//*[@id="breadcrumb-nav"]/a').text.split(' - '))== 3:
            competition_type = 'Knock Out'
            competition_stage = driver.find_element(By.XPATH, '//*[@id="breadcrumb-nav"]/a').text.split(' - ')[-1]
        else:
            print('Getting more than 3 types of information about the competition.')

        match_data['region'] = region
        match_data['league'] = league
        match_data['season'] = season
        match_data['competitionType'] = competition_type
        match_data['competitionStage'] = competition_stage

        driver.close()
            
        return match_data
    
    def fetch_data_matches_by_tournament(self, tournament_id):

        top_tournaments = fetch_top_tournaments()["topTournaments"]
        tournament = next((tournament for tournament in top_tournaments if tournament['id'] == tournament_id), None)

        driver = ss.constructWhoscoredWebDriver(WHOSCORED_URL_BASE + 'regions/' + str(tournament["region"]) + '/tournaments/' + str(tournament_id))
        # get script data from page source
        script_content = driver.find_element(By.XPATH, '//*[@id="layout-wrapper"]/script[1]').get_attribute('innerHTML')

        # clean script content
        script_content = re.sub(r"[\n\t]*", "", script_content)

        # this will give script content in list form 
        script_content_list = list(filter(None, script_content.strip().split(',            ')))
        return script_content_list
    
        metadata = script_content_list.pop(0) 

        # string format to json format
        matches_data = json.loads(metadata[metadata.index('{'):])
        keys = [item[:item.index(':')].strip() for item in script_content_list]
        values = [item[item.index(':')+1:].strip() for item in script_content_list]
        for key,val in zip(keys, values):
            matches_data[key] = json.loads(val)

        return matches_data