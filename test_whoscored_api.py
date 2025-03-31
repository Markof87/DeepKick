import warnings
import pandas as pd
import time
import re
import json
import numpy as np
from mplsoccer.pitch import Pitch, VerticalPitch
from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
pd.options.mode.chained_assignment = None
from bs4 import BeautifulSoup as soup
try:
    from tqdm import trange
except ModuleNotFoundError:
    pass

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

main_url = 'https://1xbet.whoscored.com/'

def getLeagueUrls(minimize_window=True):

    #browser_options = ChromeOptions()
    browser_options = EdgeOptions()
    browser_options.add_argument("--headless=new")  # Nuova modalità headless più compatibile
    browser_options.add_argument("--disable-blink-features=AutomationControlled")  # Nasconde Selenium
    browser_options.add_argument("--window-size=1920x1080")  # Imposta una finestra visibile
    browser_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")  # Simula un utente reale
    browser_options.add_argument("--disable-gpu")  
    browser_options.add_argument("--no-sandbox")  
    browser_options.add_argument("--disable-dev-shm-usage")  
    browser_options.add_argument("--enable-unsafe-swiftshader")  

    #driver = webdriver.Chrome(options=browser_options)
    driver = webdriver.Edge(options=browser_options)

    # Nascondere il WebDriver
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    if minimize_window:
        driver.minimize_window()

    try:
        driver.get(main_url)
    except WebDriverException:
        driver.get(main_url)

    try:
        cookie_button = driver.find_element(By.XPATH, '//*[@id="qc-cmp2-container"]/div/div/div/div[2]/div/button[2]')
        driver.execute_script("arguments[0].click();", cookie_button)
    except NoSuchElementException:
        pass

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
    df_tournaments.to_csv('tournaments.csv', index=False)

    driver.close()
    return df_tournaments

def getMatchData(url, minimize_window=True):

    #browser_options = ChromeOptions()
    browser_options = EdgeOptions()
    browser_options.add_argument("--headless=new")  # Nuova modalità headless più compatibile
    browser_options.add_argument("--disable-blink-features=AutomationControlled")  # Nasconde Selenium
    browser_options.add_argument("--window-size=1920x1080")  # Imposta una finestra visibile
    browser_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")  # Simula un utente reale
    browser_options.add_argument("--disable-gpu")  
    browser_options.add_argument("--no-sandbox")  
    browser_options.add_argument("--disable-dev-shm-usage")  
    browser_options.add_argument("--enable-unsafe-swiftshader")  

    #driver = webdriver.Chrome(options=browser_options)
    driver = webdriver.Edge(options=browser_options)

    # Nascondere il WebDriver
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    if minimize_window:
        driver.minimize_window()

    try:
        driver.get(url)
    except WebDriverException:
        driver.get(url)

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

    pass_events = [event for event in match_data["events"] if event["type"]["displayName"] == "Pass"]
    with open("passes.json", "w", encoding="utf-8") as f:
        json.dump(match_data, f, ensure_ascii=False, indent=4)

    team = 'Germany'
    teamId = 343
    opponent = 'Italy'

    getTeamTotalPasses(events_ls, teamId, team, opponent, pitch_color='#FFFFFF')

    driver.close()
        
    return match_data

def findMatches(url, minimize_window=True):

    #browser_options = ChromeOptions()
    browser_options = EdgeOptions()
    browser_options.add_argument("--headless=new")  # Nuova modalità headless più compatibile
    browser_options.add_argument("--disable-blink-features=AutomationControlled")  # Nasconde Selenium
    browser_options.add_argument("--window-size=1920x1080")  # Imposta una finestra visibile
    browser_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")  # Simula un utente reale
    browser_options.add_argument("--disable-gpu")  
    browser_options.add_argument("--no-sandbox")  
    browser_options.add_argument("--disable-dev-shm-usage")  
    browser_options.add_argument("--enable-unsafe-swiftshader")  

    #driver = webdriver.Chrome(options=browser_options)
    driver = webdriver.Edge(options=browser_options)

    # Nascondere il WebDriver
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    if minimize_window:
        driver.minimize_window()

    try:
        driver.get(url)
    except WebDriverException:
        driver.get(url)

    # get script data from page source
    script_content = driver.find_element(By.XPATH, '//*[@id="layout-wrapper"]/script[1]').get_attribute('innerHTML')


    # clean script content
    script_content = re.sub(r"[\n\t]*", "", script_content)
    print(script_content)

def getTeamTotalPasses(events_df, teamId, team, opponent, pitch_color):
    """
    Parameters
    ----------
    events_df : DataFrame of all events.
    teamId : ID of the team, the passes of which are required.
    team : Name of the team, the passes of which are required.
    opponent : Name of opponent team.
    pitch_color : color of the pitch.
    Returns
    -------
    Pitch Plot with enhanced aesthetics.
    """

    font_path = 'resources/fonts/Druk-Wide-Web-Bold-Regular.ttf' 
    custom_font = fm.FontProperties(fname=font_path)

    # Filter passes
    passes_df = events_df.loc[events_df['type'] == 'Pass'].reset_index(drop=True)
    team_passes = passes_df.loc[passes_df['teamId'] == teamId]
    
    successful_passes = team_passes.loc[team_passes['outcomeType'] == 'Successful'].reset_index(drop=True)
    unsuccessful_passes = team_passes.loc[team_passes['outcomeType'] == 'Unsuccessful'].reset_index(drop=True)
    
    # Setup the pitch with a dark background
    pitch = VerticalPitch(pitch_type='statsbomb', pitch_color=pitch_color, line_color='#4c566a', 
                  linewidth=1.5, stripe=False)
    fig, ax = pitch.draw(figsize=(6.5, 10))
    
    # Plot successful passes with a vibrant color
    pitch.arrows(successful_passes.x/100*120, 80-successful_passes.y/100*80,
                 successful_passes.endX/100*120, 80-successful_passes.endY/100*80,
                 width=1.5, headwidth=10, headlength=10, color='#32CD32', ax=ax, alpha=0.6, label="completed")
    
    # Plot unsuccessful passes with a faded color
    pitch.arrows(unsuccessful_passes.x/100*120, 80-unsuccessful_passes.y/100*80,
                 unsuccessful_passes.endX/100*120, 80-unsuccessful_passes.endY/100*80,
                 width=1.5, headwidth=8, headlength=8, color='#FF0000', ax=ax, alpha=0.6, label="blocked")
    
    ax.legend(facecolor=pitch_color, handlelength=5, edgecolor='None', fontsize=8, loc='lower left', shadow=True, labelcolor='black')
    
    # Add title
    fig.text(0.1, 0.95, f'{team} Passes vs {opponent}', fontsize=16, color='black', fontweight='bold', fontproperties=custom_font)
    fig.text(0.1, 0.93, 'Data Source: WhoScored/Opta', fontsize=10, color='black', fontstyle='italic', fontproperties=custom_font)

    orientation_arrow = FancyArrowPatch((-3, 40), (-3, 80), arrowstyle='-|>', color='black', lw=2, mutation_scale=20)
    ax.add_patch(orientation_arrow)
    
    # Set background color
    fig.patch.set_facecolor(pitch_color)
    plt.savefig("match_pass_map.png", dpi=300, bbox_inches='tight')

    plt.show()

def createEventsDF(data):
    events = data['events']
    for event in events:
        event.update({'matchId' : data['matchId'],
                        'startDate' : data['startDate'],
                        'startTime' : data['startTime'],
                        'score' : data['score'],
                        'ftScore' : data['ftScore'],
                        'htScore' : data['htScore'],
                        'etScore' : data['etScore'],
                        'venueName' : data['venueName'],
                        'maxMinute' : data['maxMinute']})
    events_df = pd.DataFrame(events)

    # clean period column
    events_df['period'] = pd.json_normalize(events_df['period'])['displayName']

    # clean type column
    events_df['type'] = pd.json_normalize(events_df['type'])['displayName']

    # clean outcomeType column
    events_df['outcomeType'] = pd.json_normalize(events_df['outcomeType'])['displayName']

    # clean outcomeType column
    try:
        x = events_df['cardType'].fillna({i: {} for i in events_df.index})
        events_df['cardType'] = pd.json_normalize(x)['displayName'].fillna(False)
    except KeyError:
        events_df['cardType'] = False

    eventTypeDict = data['matchCentreEventTypeJson']  
    events_df['satisfiedEventsTypes'] = events_df['satisfiedEventsTypes'].apply(lambda x: [list(eventTypeDict.keys())[list(eventTypeDict.values()).index(event)] for event in x])

    # clean qualifiers column
    try:
        for i in events_df.index:
            row = events_df.loc[i, 'qualifiers'].copy()
            if len(row) != 0:
                for irow in range(len(row)):
                    row[irow]['type'] = row[irow]['type']['displayName']
    except TypeError:
        pass


    # clean isShot column
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)
        if 'isShot' in events_df.columns:
            events_df['isTouch'] = events_df['isTouch'].replace(np.nan, False).infer_objects(copy=False)
        else:
            events_df['isShot'] = False

        # clean isGoal column
        if 'isGoal' in events_df.columns:
            events_df['isGoal'] = events_df['isGoal'].replace(np.nan, False).infer_objects(copy=False)
        else:
            events_df['isGoal'] = False

    # add player name column
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)
        events_df.loc[events_df.playerId.notna(), 'playerId'] = events_df.loc[events_df.playerId.notna(), 'playerId'].astype(int).astype(str)    
    player_name_col = events_df.loc[:, 'playerId'].map(data['playerIdNameDictionary']) 
    events_df.insert(loc=events_df.columns.get_loc("playerId")+1, column='playerName', value=player_name_col)

    # add home/away column
    h_a_col = events_df['teamId'].map({data['home']['teamId']:'h', data['away']['teamId']:'a'})
    events_df.insert(loc=events_df.columns.get_loc("teamId")+1, column='h_a', value=h_a_col)


    # adding shot body part column
    events_df['shotBodyType'] =  np.nan
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)
        for i in events_df.loc[events_df.isShot==True].index:
            for j in events_df.loc[events_df.isShot==True].qualifiers.loc[i]:
                if j['type'] == 'RightFoot' or j['type'] == 'LeftFoot' or j['type'] == 'Head' or j['type'] == 'OtherBodyPart':
                    events_df.loc[i, 'shotBodyType'] = j['type']


    # adding shot situation column
    events_df['situation'] =  np.nan
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=FutureWarning)
        for i in events_df.loc[events_df.isShot==True].index:
            for j in events_df.loc[events_df.isShot==True].qualifiers.loc[i]:
                if j['type'] == 'FromCorner' or j['type'] == 'SetPiece' or j['type'] == 'DirectFreekick':
                    events_df.loc[i, 'situation'] = j['type']
                if j['type'] == 'RegularPlay':
                    events_df.loc[i, 'situation'] = 'OpenPlay' 

    event_types = list(data['matchCentreEventTypeJson'].keys())
    event_type_cols = pd.DataFrame({event_type: pd.Series([event_type in row for row in events_df['satisfiedEventsTypes']]) for event_type in event_types})
    events_df = pd.concat([events_df, event_type_cols], axis=1)


    return events_df

#getMatchData(main_url + 'matches/1872048/live/international-uefa-nations-league-a-2024-2025-germany-italy')
findMatches(main_url)[0]