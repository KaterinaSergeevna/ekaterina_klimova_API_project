import requests
import logging
import allure

from endpoints.base_endpoints import BaseEndpoint
from endpoints.json_schemas import DataModel

logging.getLogger(__name__)
logging.basicConfig(level=logging.info('msg'))


class GetObject(BaseEndpoint):
    response_date = None
    meme_ids = []

    @allure.step('Get meme by id')
    def get_meme_by_id(self, post_id, token):
        self.response = requests.get(f"http://167.172.172.115:52355/meme/{post_id}",
                                     headers={'Authorization': token})
        self.status_code = self.response.status_code
        if self.status_code == 200:
            self.response = self.response.json()
            self.response_date = DataModel(**self.response)

    @allure.step('Check that data is equal')
    def check_that_request_data_is_equal_response_data(self, data):
        assert self.response_date.text == data['text']
        assert self.response_date.url == data['url']
        assert self.response_date.tags == data['tags']
        assert self.response_date.info.range == data['info']['range']
        assert self.response_date.info.colors == data['info']['colors']

    @allure.step('Check that token is still valid')
    def check_token_is_valid(self, token):
        self.response = requests.get(f"http://167.172.172.115:52355/authorize/{token}")
        assert "Token is alive" in self.response.text, f"requires authorization"

    @allure.step('Try to get meme by id without authorization')
    def get_meme_by_id_without_token(self, post_id):
        self.response = requests.get(f"http://167.172.172.115:52355/meme/{post_id}")
        self.status_code = self.response.status_code

    @allure.step('Try to get all memes without authorization')
    def get_meme_without_token(self):
        self.response = requests.get(f"http://167.172.172.115:52355/meme")
        self.status_code = self.response.status_code

    @allure.step('Check that request id and response id is equal')
    def check_that_id_is(self, post_id):
        assert self.response_date.id == post_id

    @allure.step('Check by id that all memes are correct')
    def check_that_all_meme_is_correct(self, token):
        flag = 1
        for id in self.meme_ids:
            self.get_meme_by_id(id, token)
            logging.info(f'status code for {id} is {self.status_code}')
            if self.status_code != 200:
                flag = 0
        assert flag == 1

    @allure.step('Send get request for all memes')
    def get_all_meme(self, token):
        self.response = requests.get(f"http://167.172.172.115:52355/meme", headers={'Authorization': token})
        self.status_code = self.response.status_code

    @allure.step('Get all ids')
    def get_all_id_for_meme(self, token):
        all_memes = requests.get("http://167.172.172.115:52355/meme", headers={'Authorization': token}).json()
        self.meme_ids = [int(i["id"]) for i in all_memes["data"]]
        return self.meme_ids
