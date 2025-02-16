from flask import Flask, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()
app = Flask(__name__)

STEAM_API_KEY = os.environ.get("API_KEY")

@app.route('/api/user/<steam_id>')
def get_user_info(steam_id):
    url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={steam_id}'
    print(url)
    resp = requests.get(url)
    if resp.status_code == 200:
        return jsonify(resp.json())
    else:
        return jsonify({'error': 'Failed to fetch user data'}), 500

if __name__ == '__main__':
    app.run(debug=True)