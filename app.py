from flask import Flask, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()
app = Flask(__name__)

STEAM_API_KEY = os.environ.get("API_KEY")

@app.route('/api/user/<steam_id>')
def get_user_info(steam_id):
    print(steam_id)
    print(STEAM_API_KEY)
    return jsonify({'success': '555'})

if __name__ == '__main__':
    app.run(debug=True)