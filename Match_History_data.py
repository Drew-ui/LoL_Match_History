from riotwatcher import LolWatcher, ApiError
import pandas as pd
from datetime import datetime

def get_api_key():
    f = open("Riot_API_Key.txt", "r")
    return f.read()

# Global variables
api_key = get_api_key()
watcher = LolWatcher(api_key)
my_region = 'euw1'
summ = 'Lâd' # str(input('Summoner Name: '))

# Find summoner
me = watcher.summoner.by_name(my_region, summ)

# Fetch my matches
my_matches = watcher.match.matchlist_by_puuid(my_region, me['puuid'])

# Collect match data
def create_match_data(index):
    last_match = my_matches[index]
    match_detail = watcher.match.by_id(my_region, last_match)

    participants = []

    for puid in match_detail['metadata']['participants']:
        participants.append(watcher.summoner.by_puuid(my_region, puid)['name'])

    par = [i for i in participants]
    champ1 = [i['championName'] for i in match_detail['info']['participants']] # Collect champion name
    role1 = [i['individualPosition'] for i in match_detail['info']['participants']] # Collect role name
    kills = [i['kills'] for i in match_detail['info']['participants']] # Collect kill amount
    deaths1 = [i['deaths'] for i in match_detail['info']['participants']] # Collect death amount
    assists1 = [i['assists'] for i in match_detail['info']['participants']] # Collect assists amount
    wards1 = [i['wardsPlaced'] for i in match_detail['info']['participants']] # Collect wards amount
    gold = [i['goldEarned'] for i in match_detail['info']['participants']] # Collect gold amount
    minions = [i['totalMinionsKilled'] for i in match_detail['info']['participants']] # Collect minions killed amount
    neu_minions = [i['neutralMinionsKilled'] for i in match_detail['info']['participants']] # Collect neutral minions killed amount
    creeps1 = [x + y for x, y in zip(minions, neu_minions)] # Collect total farm amount
    damage_total = [i['totalDamageDealtToChampions'] for i in match_detail['info']['participants']] # Collect total damage dealt amount
    damage_recieve = [i['totalDamageTaken'] for i in match_detail['info']['participants']] # Collect total damage recieved amount
    win = [i['win'] for i in match_detail['info']['participants']] # Collect win/loss

    # Create data dictionary
    data = {
        'Game_ID': last_match,
        'Summoner': par,
        'Champion': champ1,
        'Role': role1,
        'Kills': kills,
        'Deaths': deaths1,
        'Assists': assists1,
        'Wards': wards1,
        'Gold Earned': gold,
        'Farm': creeps1,
        'Total Damage Dealt': damage_total,
        'Total Taken Damage': damage_recieve,
        'Result': win
    }
    return data

# Create dataframes of match data for last 50 games and save to .csv:
for i in range(0,50):
    df = pd.DataFrame(create_match_data(i))
    file = 'game_data' + str(i) + '.csv'
    df.to_csv(file)
    print(file + ' ' + 'saved')

# Collect Game time data
def create_match_time_data(index):
    last_match = my_matches[index]
    match_detail = watcher.match.by_id(my_region, last_match)
    game_start = datetime.fromtimestamp(match_detail['info']['gameStartTimestamp']/1000) # Collect game start time
    game_start = game_start.strftime("%m/%d/%Y - %H:%M:%S")
    game_end = datetime.fromtimestamp(match_detail['info']['gameEndTimestamp'] / 1000) # Collect game end time
    game_end = game_end.strftime("%m/%d/%Y - %H:%M:%S")

    # Create data dictionary
    data2 = {
        'Game_ID': [last_match],
        'Game_Start_Time': [game_start],
        'Game_End_Time': [game_end],
    }
    return data2

# Create dataframes of game time for last 20 games and save to .csv:
for i in range(0,50):
    df = pd.DataFrame(create_match_time_data(i))
    file = 'time_data' + str(i) + '.csv'
    df.to_csv(file)
    print(file + ' ' + 'saved')