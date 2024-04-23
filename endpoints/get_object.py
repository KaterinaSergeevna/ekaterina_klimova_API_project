import requests
import allure
from endpoints.base_endpoints import BaseEndpoint
from endpoints.json_schemas import DataModel


class GetObject(BaseEndpoint):
    response_date = None

    def get_meme_by_id(self, post_id, token):
        self.response = requests.get(f"http://167.172.172.115:52355/meme/{post_id}",
                                     headers={'Authorization': token})
        self.status_code = self.response.status_code
        self.response = self.response.json()
        if self.status_code != 404:
            self.response_date = DataModel(**self.response)

    def check_that_id_is(self, post_id):
        assert self.response_date.id == post_id

    def check_token_is_valid(self, token):
        self.response = requests.get(f"http://167.172.172.115:52355/authorize/{token}")
        assert "Token is alive" in self.response.text, f"requires authorization"

    def get_meme_by_id_without_token(self, post_id):
        self.response = requests.get(f"http://167.172.172.115:52355/meme/{post_id}")
        self.status_code = self.response.status_code

    @allure.step('Check id')
    def check_that_id_is(self, post_id):
        assert self.response_date.id == post_id
