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
        json_loaded_response = json.loads(response.text)
        split : list[str] = filters.split(',')
        if(json_loaded_response[f'{app_id}']['success']):
            try:
                del json_loaded_response[f'{app_id}']['data']['type']
            except:
                pass
            try:
                del json_loaded_response[f'{app_id}']['data']['pc_requirements']
            except:
                pass
            try:
                del json_loaded_response[f'{app_id}']['data']['legal_notice']
            except:
                pass
            try:
                del json_loaded_response[f'{app_id}']['data']['about_the_game']
            except:
                pass
            try:
                del json_loaded_response[f'{app_id}']['data']['detailed_description']
            except:
                pass
            try:
                del json_loaded_response[f'{app_id}']['data']['drm_notice']
            except:
                pass
            try:
                del json_loaded_response[f'{app_id}']['data']['capsule_imagev5']
            except:
                pass
            try:
                del json_loaded_response[f'{app_id}']['data']['capsule_image']
            except:
                pass
            try:
                del json_loaded_response[f'{app_id}']['data']['required_age']
            except:
                pass
            try:
                del json_loaded_response[f'{app_id}']['data']['linux_requirements']
            except:
                pass
            try:
                del json_loaded_response[f'{app_id}']['data']['mac_requirements']
            except:
                pass
            try:
                del json_loaded_response[f'{app_id}']['data']['reviews']
            except:
                pass
            try:
                del json_loaded_response[f'{app_id}']['data']['short_description']
            except:
                pass
            try:
                del json_loaded_response[f'{app_id}']['data']['supported_languages']
            except:
                pass
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
            if('price_overview' in split and json_loaded_response[f'{app_id}']['data']['is_free']):
                try:
                    del json_loaded_response[f'{app_id}']['data']['price_overview']
                except:
                    pass


        
        return json_loaded_response
    
    
    
    



