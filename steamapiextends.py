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
            if('name' in split and len(split) == 1):
                try:
                    name = list(json_loaded_response.keys())[0]
                    json_loaded_response[f'name'] = name
                    for key in list(json_loaded_response.keys()):
                        if(key != 'name'):
                            json_loaded_response.pop(key)
                    json_loaded_response = list(json_loaded_response.keys())
                except:
                    pass
        
        return json_loaded_response
    
    
    
    



