import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.config_system import SOCCERDATA_DIR

import soccerdata as sd
import json
from pathlib import Path

league_dict_path = Path(SOCCERDATA_DIR) / 'config' / 'league_dict.json'
resources_path = Path(__file__).parent.parent / 'resources' / 'json' / 'allTournaments.json'

if not league_dict_path.exists():
    league_dict_path.parent.mkdir(parents=True, exist_ok=True)
    with resources_path.open('r', encoding='utf-8') as src_file:
        data = json.load(src_file)
    with league_dict_path.open('w', encoding='utf-8') as dest_file:
        json.dump(data, dest_file, indent=4)

print(sd.FBref.available_leagues())
