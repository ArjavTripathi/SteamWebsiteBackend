from flask import Flask, jsonify
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()
app = Flask(__name__)

STEAM_API_KEY = os.environ.get("API_KEY")
#good json parser = https://jsongrid.com/json-parser
@app.route('/game/<app_id>')
def get_app_name(app_id):
    url = f'http://store.steampowered.com/api/appdetails/?appids={app_id}'
    resp = requests.get(url)
    data = resp.json()
    gameName = data[str(app_id)]['data']
    toReturn = {}
    toReturn['name'] = gameName['name']
    toReturn['icon'] = gameName['capsule_image']
    toReturn['isFree'] = gameName['is_free']
    toReturn['genres'] = gameName['genres']
    toReturn['url'] = gameName['website']
    print(toReturn)
    
    if resp.status_code == 200:
        return jsonify(gameName)
    else:
        return jsonify({'error': 'Failed to fetch user data'}), 500


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
    gameid = []
    for game in games:
        appid = game.get('appid')
        gameid.append(appid)
        print(f"AppID: {appid}")
    return gameid

    

if __name__ == '__main__':
    app.run(debug=True)