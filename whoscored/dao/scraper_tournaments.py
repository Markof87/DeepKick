import re
import json
import pandas as pd
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.by import By

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from whoscored.helpers import createEventsDF

from scraper_service import main_url

import scraper_service as ss

def getAllLeaguesDF(url):
    #TODO: da valutare se portare fuori il driver
    driver = ss.constructWhoscoredWebDriver(url)

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

def getMatchData(url):
    
    driver = ss.constructWhoscoredWebDriver(url)
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

    events_ls = createEventsDF(match_data)

    return events_ls

    pass_events = [event for event in match_data["events"] if event["type"]["displayName"] == "Pass"]
    with open("passes.json", "w", encoding="utf-8") as f:
        json.dump(match_data, f, ensure_ascii=False, indent=4)

    team = 'England'
    teamId = 345
    opponent = 'Latvia'

    getTeamTotalPasses(events_ls, teamId, team, opponent, pitch_color='#000000')

    driver.close()
        
    return match_data

print(getMatchData(main_url + 'matches/1874074/live/international-world-cup-qualification-uefa-2025-2026-england-latvia'))