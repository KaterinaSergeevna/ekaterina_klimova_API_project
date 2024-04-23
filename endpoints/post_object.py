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
    'text': 'example for test',
    'url': 'http://tratatata',
    'tags': ["hehe", "just for fun"],
    'info': {"color": "red", "range": 7}
}


class PostObject(BaseEndpoint):
    token = None

    def take_token(self):
        self.response = requests.post("http://167.172.172.115:52355/authorize", json={"name": "Kate"})
        self.response_json = self.response.json()


    def take_token_for_other_name(self, creads=None):
        logging.info(f'[take_token] Creads is {creads}')
        self.response = requests.post("http://167.172.172.115:52355/authorize", json=creads)
        self.status_code = self.response.status_code
        logging.info(f'[take_token] status code is {self.status_code}')

    @allure.step('Send post request')
    def create_meme(self, payload=None, headers=None):
        headers = headers if headers else HEADERS
        payload = payload if payload else PAYLOAD
        self.response = requests.post("http://167.172.172.115:52355/meme", json=payload,
                                      headers={"Authorization": self.token})
        self.status_code = self.response.status_code
        self.response_json = self.response.json()

    def post_meme_without_token(self, payload=None):
        payload = payload if payload else PAYLOAD
        self.response = requests.post(f"http://167.172.172.115:52355/meme", json=payload)
        self.status_code = self.response.status_code

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
