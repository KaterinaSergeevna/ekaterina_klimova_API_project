import requests
import allure
from endpoints.base_endpoints import BaseEndpoint
from endpoints.json_schemas import DataModel

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.info('msg'))


class PutObject(BaseEndpoint):

    @allure.step('Send put request')
    def send_put_request(self, p_id, token):
        put_payload = {
            "id": p_id,
            "url": "https://new",
            "text": "Piu",
            "tags": [
                "piu12",
                "pi-piu12"
            ],
            "info": {
                "colors": ["222fdghgh2222"],
                "range": 11111
            }
        }
        self.response = requests.put(f"http://167.172.172.115:52355/meme/{p_id}", json=put_payload,
                                     headers={"Authorization": token})
        self.status_code = self.response.status_code
        self.response_json = self.response.json()
        return self.response_json['id']

    @allure.step('Try to send put request without authorization')
    def put_meme_without_token(self, p_id):
        put_payload = {
            "id": p_id,
            "url": "https://new",
            "text": "Piu",
            "tags": [
                "piu12",
                "pi-piu12"
            ],
            "info": {
                "colors": ["222fdghgh2222"],
                "range": 11111
            }
        }
        self.response = requests.put(f"http://167.172.172.115:52355/meme/{p_id}", json=put_payload)
        self.status_code = self.response.status_code

    @allure.step('Try to send put request with incorrect data')
    def put_meme_with_incorrect_data(self, token, p_id, put_payload):
        logging.info(f'[put_meme_with_incorrect_data] payload is  is {put_payload}')
        self.response = requests.put(f"http://167.172.172.115:52355/meme/{p_id}", json=put_payload,
                                     headers={"Authorization": token})
        self.status_code = self.response.status_code
        logging.info(f'[put_meme_with_incorrect_data] status code is {self.status_code}')

    @allure.step('Try to change other meme')
    def send_put_request_to_other_meme(self, token):
        put_payload = {
            "id": 2,
            "url": "https://new",
            "text": "Piu",
            "tags": [
                "piu12",
                "pi-piu12"
            ],
            "info": {
                "colors": ["222fdghgh2222"],
                "range": 11111
            }
        }
        self.response = requests.put(f"http://167.172.172.115:52355/meme/2", json=put_payload,
                                     headers={"Authorization": token})
        self.status_code = self.response.status_code
