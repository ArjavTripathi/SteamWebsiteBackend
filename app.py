from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()
app = Flask(__name__)

STEAM_API_KEY = os.environ.get("API_KEY")
#good json parser = https://jsongrid.com/json-parser

def get_app_info(app_id):
    url = f'http://store.steampowered.com/api/appdetails/?appids={app_id}'
    resp = requests.get(url)
    data = resp.json()
    try:
        gameName = data[str(app_id)]['data']
    except:
        return jsonify({'error': 'Failed to fetch game data'}), 500
    
    toReturn = build_dict(gameName)
    
    return toReturn


@app.route('/user/<steam_id>')
def get_game_info(steam_id):
    url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={steam_id}'
    resp = requests.get(url)
    resp_games = get_game_names(resp.json())
    if resp.status_code == 200:
        return jsonify(resp_games)
    else:
        return jsonify({'error': 'Failed to fetch user data'}), 500


def get_game_names(resp):
    games = resp.get('response', {}).get('games', [])
    gameInfo = {}
    for game in games:
        appid = game.get('appid')
        gameInfo[f'{appid}'] = get_app_info(appid)
    return gameInfo

def build_dict(gameName):
    toReturn = {}
    #Useful Data about Game to Return
    toReturn['name'] = gameName['name']
    toReturn['icon'] = gameName['capsule_image']
    toReturn['isFree'] = gameName['is_free']
    try:
        toReturn['criticRating'] = gameName['metacritic']['score']
    except:
        pass
    try:
        toReturn['url'] = gameName['website']
    except:
        toReturn['url'] = f'steamcommunity.com/app/{app_id}'
    toReturn['genres'] = [genre['description'] for genre in gameName['genres']]
    #Gets useful categories ONLY
    categories = gameName.get('categories', [])
    result = []
    wantedCategories = ['Single-player', 'Multi-player', 'Co-op', 'Online Co-op', 'Full controller support', 'Family Sharing']
    for category in categories:
        if category['description'] in wantedCategories:
            result.append(category['description'])
    toReturn['categories'] = result
    toReturn['platforms'] = gameName['platforms']
    if not toReturn['isFree']:
        try:
            toReturn['PriceCurrency'] = gameName['price_overview']['currency']
            toReturn['priceAmount'] = gameName['price_overview']['initial']
        except:
            pass
    return toReturn
        

@app.route('/test/<app_id>')
def full_json(app_id):
    url = f'http://store.steampowered.com/api/appdetails/?appids={app_id}'
    resp = requests.get(url)
    data = resp.json()
    gameName = data[str(app_id)]['data']
    if resp.status_code == 200:
        return jsonify(gameName)
    else:
        return jsonify({'error': 'Failed to fetch game data'}), 500


    

if __name__ == '__main__':
    app.run(debug=True)