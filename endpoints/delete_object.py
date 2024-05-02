import requests
import allure
from endpoints.base_endpoints import BaseEndpoint


class DeleteObject(BaseEndpoint):

    @allure.step('Delete meme by id')
    def delete_meme(self, token, post_id=None):
        self.response = requests.delete(f"http://167.172.172.115:52355/meme/{post_id}",
                                        headers={'Authorization': token})
        self.status_code = self.response.status_code

    @allure.step('Try to delete meme with unreal id')
    def delete_meme_with_unreal_id(self, token):
        self.response = requests.delete(f"http://167.172.172.115:52355/meme/0",
                                        headers={'Authorization': token})
        self.status_code = self.response.status_code

    @allure.step('Try to delete meme without authorization')
    def delete_without_token(self, post_id):
        self.response = requests.delete(f"http://167.172.172.115:52355/meme/{post_id}")
        self.status_code = self.response.status_code

    @allure.step('Try to delete all meme')
    def delete_all_memes(self, token):
        self.response = requests.delete(f"http://167.172.172.115:52355/meme/",
                                        headers={'Authorization': token})
        self.status_code = self.response.status_code
