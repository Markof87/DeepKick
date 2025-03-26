import unittest
import pandas as pd

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from shared.utils import createEventsDF
class TestCreateEventsDF(unittest.TestCase):
    def setUp(self):
        # Dati di esempio per il test
        self.data = {
            'events': [
                {
                    'eventId': 1,
                    'period': {'displayName': 'FirstHalf'},
                    'type': {'displayName': 'Pass'},
                    'outcomeType': {'displayName': 'Successful'},
                    'cardType': None,
                    'qualifiers': [{'type': {'displayName': 'RightFoot'}}],
                    'isShot': False,
                    'playerId': 101,
                    'teamId': 201,
                    'satisfiedEventsTypes': [1]  # Aggiungi questa chiave

                },
                {
                    'eventId': 2,
                    'period': {'displayName': 'SecondHalf'},
                    'type': {'displayName': 'Shot'},
                    'outcomeType': {'displayName': 'Goal'},
                    'cardType': None,
                    'qualifiers': [{'type': {'displayName': 'LeftFoot'}}],
                    'isShot': True,
                    'playerId': 102,
                    'teamId': 202,
                    'satisfiedEventsTypes': [2]  # Aggiungi questa chiave

                }
            ],
            'matchId': 12345,
            'startDate': '2025-03-26',
            'startTime': '20:00',
            'score': '2-1',
            'ftScore': '2-1',
            'htScore': '1-0',
            'etScore': None,
            'venueName': 'Stadium',
            'maxMinute': 90,
            'playerIdNameDictionary': {101: 'Player A', 102: 'Player B'},
            'home': {'teamId': 201},
            'away': {'teamId': 202},
            'matchCentreEventTypeJson': {'Pass': 1, 'Shot': 2}
        }

    def test_create_events_df(self):
        # Esegui la funzione
        events_df = createEventsDF(self.data)

        # Testa il numero di righe
        self.assertEqual(len(events_df), 2)

        # Testa le colonne
        expected_columns = [
            'eventId', 'period', 'type', 'outcomeType', 'cardType', 'qualifiers',
            'isShot', 'playerId', 'playerName', 'teamId', 'h_a', 'shotBodyType',
            'situation', 'Pass', 'Shot'
        ]
        for col in expected_columns:
            self.assertIn(col, events_df.columns)

        # Testa i valori specifici
        self.assertEqual(events_df.loc[0, 'playerName'], 'Player A')
        self.assertEqual(events_df.loc[1, 'type'], 'Shot')
        self.assertEqual(events_df.loc[1, 'situation'], 'OpenPlay')

if __name__ == '__main__':
    unittest.main()