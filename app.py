from flask import Flask, jsonify, request
from dotenv import load_dotenv
from steam_web_api import Steam
from steamapiextends import extendsAPI
import os
import regex as re
import requests
import json


load_dotenv()

app = Flask(__name__)

STEAM_API_KEY = os.environ.get("API_KEY")
steam = Steam(STEAM_API_KEY)
ext = extendsAPI(STEAM_API_KEY)

        

@app.route('/test/<app_id>')
def full_json(app_id):
    url = f'http://store.steampowered.com/api/appdetails/?appids={app_id}'
    resp = requests.get(url)
    data = resp.json()
    if resp.status_code == 200:
        return jsonify(data)
    else:
        return jsonify({'error': 'Failed to fetch game data'}), 500

@app.route('/search/<search>')
def search_for_app(search):
    searching = steam.apps.search_games(search)
    return jsonify(searching)

@app.route('/gameowned')
def testgetgames():
    wantedFilter = 'categories,genres,controller_support,price_overview'
    #wantedFilter = 'name'
    gamedetails = {}
    user = steam.users.get_owned_games(os.environ.get("My_ID"))
    for game in user['games']:
            gamedetails[f'{game['name']}'] = ext.get_app_details(game['appid'], filters=wantedFilter)
        
    return jsonify(gamedetails)





if __name__ == '__main__':
    app.run(debug=True)