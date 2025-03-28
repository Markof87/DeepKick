import warnings
import numpy as np
import pandas as pd

def find_player(players_data, player_id, player_id_field):
    for player in players_data:
        if player[player_id_field] == player_id:
            return player

    return None


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