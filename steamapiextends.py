from steam_web_api import Steam, Apps, Client, constants
from requests import request, Response
import json
import regex
import typing

class extendsAPI(Apps):
    def __init__(self, key : str):
        client = Client(key, headers={})
        self.__search_url = constants.API_APP_SEARCH_URL
        self.__app_details_url = constants.API_APP_DETAILS_URL
    
    def get_app_details(self, app_id: int, country="US", filters: typing.Optional[str] = "name") -> dict:

        response = request(
            "get",
            self.__app_details_url,
            params={"appids": app_id, "cc": country, "filters": filters},
        )
        split : list[str] = filters.split(',')
        json_loaded_response = json.loads(response.text)
        if(json_loaded_response[f'{app_id}']['success']):
            if('categories' in split):
                try:
                    json_loaded_response[f'{app_id}']['data']['categories'] = [category['description'] for category in json_loaded_response[f'{app_id}']['data']['categories'] if category['description'] in {'Single-player', 'Multi-player', 'Co-op', 'Online Co-op', 'Full controller support', 'Family Sharing', 'Partial Controller Support', 'In-App Purchases', 'Cross-Platform Multiplayer', 'Shared/Split Screen', 'Remote Play on TV', 'Remote Play Together', 'VR Supported'}]
                except:
                    pass
            if('genres' in split):
                try:
                    json_loaded_response[f'{app_id}']['data']['genres'] = [genres['description'] for genres in json_loaded_response[f'{app_id}']['data']['genres']]
                except:
                    pass
            if('name' in split and len(split) == 1):
                try:
                    json_loaded_response = list(json_loaded_response.keys())
                except:
                    pass
        
        return json_loaded_response
    
    
    
    



