import requests
import allure
import pdb
from pydantic import ValidationError
from endpoints.base_endpoints import BaseEndpoint
from endpoints.json_schemas import DataModel

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.info('msg'))

HEADERS = {
    'Content-type': 'application/json',

}
PAYLOAD = {
    "text": "example for test",
    "url": "https://imgflip.com/i/8ngjno",
    "tags": [
        "piu",
        "pi-piu"
    ],
    "info": {
        "colors": ["blue"],
        "range": 9
    }
}


class PostObject(BaseEndpoint):

    @allure.step('Take token')
    def take_token(self):
        self.response = requests.post("http://167.172.172.115:52355/authorize", json={"name": "Kate"})
        self.status_code = self.response.status_code
        self.response_json = self.response.json()
        self.token = self.response_json["token"]
        with open('cread.txt', 'w') as file:
            file.write(self.token)

    @allure.step('Try to take token for name with prohibited type')
    def take_token_for_other_name(self, creads=None):
        logging.info(f'[take_token] Creads is {creads}')
        self.response = requests.post("http://167.172.172.115:52355/authorize", json=creads)
        self.status_code = self.response.status_code
        logging.info(f'[take_token] status code is {self.status_code}')

    @allure.step('Create new meme')
    def create_meme(self, token, payload=None, headers=None):
        headers = headers if headers else HEADERS
        payload = payload if payload else PAYLOAD
        self.response = requests.post("http://167.172.172.115:52355/meme", json=payload,
                                      headers={"Authorization": token})
        self.status_code = self.response.status_code
        if self.status_code == 200:
            self.response_json = self.response.json()
            return self.response_json['id']

    @allure.step('Try to create new meme without authorization')
    def post_meme_without_token(self, payload=None):
        payload = payload if payload else PAYLOAD
        self.response = requests.post(f"http://167.172.172.115:52355/meme", json=payload)
        self.status_code = self.response.status_code

    @allure.step('Check data model')
    def check_data_model(self):
        if self.status_code == 200:
            new_meme = DataModel(**self.response_json)
            try:
                new_meme.validate()
                logger.info(f"Новый мем {new_meme.id} соответствует требованиям к типам данных")
                return new_meme.id
            except ValidationError as e:
                logger.error("Ошибка в данных нового мема: %s", e)
                return None
        else:
            logger.error("Ошибка при создании мема. Код ответа: %d", self.status_code)

    @allure.step('Check that id is unicum')
    def check_that_id_is_unicum(self, meme_ids):
        assert self.response_json['id'] not in meme_ids
