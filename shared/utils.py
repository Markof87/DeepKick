import json
import sys
import os
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from shared.reports import getEventReport

import webbrowser
from PIL import Image
from io import BytesIO

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

def image_creator(url, event_name, name, opponent):

    response = requests.get(url)
    # Assicurati che la richiesta sia andata a buon fine
    if response.status_code == 200:
        match_data = response.json()
    else:
        print(f"Errore nella richiesta: {response.status_code}")

    img_buffer = getEventReport(match_data, event_name, name, opponent, pitch_color='#FFFFFF')
    img_buffer.seek(0)
    image_data = compress_image(img_buffer.read(), target_size_kb=976.56, initial_resize_factor=1.0)

    with open('temp_image.png', 'wb') as temp_file:
        temp_file.write(image_data)
    webbrowser.open('temp_image.png')

    print("Immagine salvata come debug_image.png per verifica.")

    if not image_data:
        print("Errore: Il buffer dell'immagine è vuoto.")
        exit(1)

    return match_data

def compress_image(input_image_bytes, target_size_kb=976.56, initial_resize_factor=1.0):
    """
    Comprimi l'immagine riducendone la qualità e, se necessario, la risoluzione fino a
    ottenere un file inferiore al target in KB.
    """
    # Apri l'immagine dai byte
    original_img = Image.open(BytesIO(input_image_bytes))
    
    # Converti in RGB se l'immagine ha trasparenza (PNG ad esempio)
    if original_img.mode in ("RGBA", "P"):
        original_img = original_img.convert("RGB")
    
    resize_factor = initial_resize_factor
    
    while resize_factor > 0.1:  # evitiamo di ridurre troppo l'immagine
        # Calcola le nuove dimensioni
        new_width = int(original_img.width * resize_factor)
        new_height = int(original_img.height * resize_factor)
        resized_img = original_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Prova a salvare con diverse qualità
        for quality in range(95, 9, -5):
            buffer = BytesIO()
            # Il parametro optimize=True aiuta a ridurre la dimensione del file
            resized_img.save(buffer, format="JPEG", quality=quality, optimize=True)
            size_kb = len(buffer.getvalue()) / 1024
            if size_kb <= target_size_kb:
                print(f"Compressione riuscita: qualità={quality}, resize_factor={resize_factor:.2f}, dimensione={size_kb:.2f}KB")
                return buffer.getvalue()
        # Se non siamo riusciti a scendere al di sotto del target, riduci ulteriormente la risoluzione
        resize_factor *= 0.8
        print(f"Riduzione della risoluzione: nuovo resize_factor={resize_factor:.2f}")
    
    print("Impossibile comprimere l'immagine al di sotto del limite richiesto.")
    return None