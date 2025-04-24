import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import json
import soccerdata as sd
from fbref.utils.utils import restructure_json
from shared.config_system import SOCCERDATA_DIR

from pathlib import Path

league_dict_path = Path(SOCCERDATA_DIR) / 'config' / 'league_dict.json'

class FBrefService():
    def __init__(self):
        pass

    def get_teamseason_base_stats(self, tournament, season):
        tournament_data = None
        if league_dict_path.exists():
            with open(league_dict_path, 'r') as file:
                league_data = json.load(file)
                tournament_data = next((key for key, value in league_data.items() if value.get("ClubElo") == tournament), None)
                #tournament_data = next((item for item in league_data if item.get("ClubElo") == tournament), None)
                print(tournament_data)

        if tournament_data is None:
            match tournament:
                case "ENG":
                    tournament_data = "ENG-Premier League"
                case "GER":
                    tournament_data = "GER-Bundesliga"
                case "ESP":
                    tournament_data = "ESP-La Liga"
                case "ITA":
                    tournament_data = "ITA-Serie A"
                case "FRA":
                    tournament_data = "FRA-Ligue 1"
                case "BIG5":
                    tournament_data = "Big 5 European Leagues Combined"
                case _:
                    raise ValueError(f"Unsupported tournament: {tournament}")

        season = sd.FBref(tournament_data, season)
        json_str = season.read_team_season_stats().to_json()
        data = json.loads(json_str)
        return restructure_json(data)
