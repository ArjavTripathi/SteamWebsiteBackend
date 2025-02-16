from flask import Flask, jsonify, request
from dotenv import load_dotenv
from steam_web_api import Steam
from steamapiextends import extendsAPI
import os
import requests
import json

load_dotenv()

app = Flask(__name__)

STEAM_API_KEY = os.environ.get("API_KEY")
steam = Steam(STEAM_API_KEY)
ext = extendsAPI(STEAM_API_KEY)
#good json parser = https://jsongrid.com/json-parser

# def get_app_info(app_id):
#     url = f'http://store.steampowered.com/api/appdetails/?appids={app_id}'
#     resp = requests.get(url)
#     data = resp.json()
#     if not data[f'{app_id}']['success']:
#         return False        
#     try:
#         gameName = data[str(app_id)]['data']
#     except:
#         return jsonify({'error': 'Failed to fetch game data'}), 500
    
#     toReturn = build_dict(gameName)
    
#     return toReturn


# @app.route('/user/<steam_id>')
# def get_game_info(steam_id):
#     url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={steam_id}'
#     resp = requests.get(url)
#     resp_games = get_game_names(resp.json())
#     if resp.status_code == 200:
#         return jsonify(resp_games)
#     else:
#         return jsonify({'error': 'Failed to fetch user data'}), 500


# def get_game_names(resp):
#     games = resp.get('response', {}).get('games', [])
#     merged = {}
#     for game in games:
#         try:
#             appid = game.get('appid')
#             if not get_app_info(appid): #checks if data exists
#                 continue
#             game_info = get_app_info(appid)  # This returns the game data
#             merged[f'{game_info['name']}'] = game_info
#         except:
#             pass
    



    # Return the JSON serialized object
    # return json.dumps(merged)
    



# def build_dict(gameName):
#     toReturn = {}
#     #Useful Data about Game to Return
#     toReturn['name'] = gameName['name']
#     toReturn['icon'] = gameName['capsule_image']
#     toReturn['isFree'] = gameName['is_free']
#     try:
#         toReturn['criticRating'] = gameName['metacritic']['score']
#     except:
#         pass
#     try:
#         toReturn['url'] = gameName['website']
#     except:
#         toReturn['url'] = f'steamcommunity.com/app/{app_id}'
#     toReturn['genres'] = [genre['description'] for genre in gameName['genres']]
#     #Gets useful categories ONLY
#     categories = gameName.get('categories', [])
#     result = []
#     wantedCategories = ['Single-player', 'Multi-player', 'Co-op', 'Online Co-op', 'Full controller support', 'Family Sharing']
#     for category in categories:
#         if category['description'] in wantedCategories:
#             result.append(category['description'])
#     toReturn['categories'] = result
#     toReturn['platforms'] = gameName['platforms']
#     if not toReturn['isFree']:
#         try:
#             toReturn['PriceCurrency'] = gameName['price_overview']['currency']
#             toReturn['priceAmount'] = gameName['price_overview']['initial']
#         except:
#             pass
#     return toReturn
        

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
    #wantedFilter = 'categories,genres,controller_support,price_overview'
    wantedFilter = 'name'
    gamedetails = {}
    user = steam.users.get_owned_games(os.environ.get("My_ID"))
    for game in user['games']:
            gamedetails[f'{game['name']}'] = ext.get_app_details(game['appid'], filters=wantedFilter)
    
    with open('appidGameNames.json', 'w') as f:
          json.dump(gamedetails, f, indent=4)
        
    return jsonify(gamedetails)

@app.route('/testdata')
def formatTestData():
     with open('newAPIdata.json', 'r') as f:
          json_loaded_response = json.load(f)

     
     with open('appidOwnedGames.json', 'r') as f:
         testData = json.load(f)


     split = 'categories,genres,controller_support,price_overview'.split(',')
     
     
     for app_id in testData:
        if(json_loaded_response[f'{app_id}']['success']):
            if('categories' in split):
                try:
                    json_loaded_response[f'{app_id}']['data']['categories'] = [category['description'] for category in json_loaded_response[f'{app_id}']['data']['categories']]
                except:
                    pass
            if('genres' in split):
                try:
                    json_loaded_response[f'{app_id}']['data']['genres'] = [genres['description'] for genres in json_loaded_response[f'{app_id}']['data']['genres']]
                except:
                    pass
            if('price_overview' in split):
                try:
                    json_loaded_response[f'{app_id}']['data']['price_overview'] = [{'currency': price['currency'], 'initial': price['initial']} for price in json_loaded_response[f'{app_id}']['data']['price_overview']]
                except:
                    pass
    
     return jsonify(json_loaded_response) 


if __name__ == '__main__':
    app.run(debug=True)