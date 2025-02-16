from steam_web_api import Steam, Apps, Client, constants
from requests import request, Response
import json
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
        return json_loaded_response


