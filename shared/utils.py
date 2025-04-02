import json
import os

def fetch_top_tournaments():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'json', 'topTournaments.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding JSON from file: {file_path}")

def find_player(players_data, player_id, player_id_field):
    for player in players_data:
        if player[player_id_field] == player_id:
            return player

    return None
