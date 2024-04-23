import requests
from endpoints.base_endpoints import BaseEndpoint


class DeleteObject(BaseEndpoint):

    def delete_meme(self, post_id):
        self.response = requests.delete(f"http://167.172.172.115:52355/meme/{post_id}",
                                        headers={'Authorization': self.token})
        self.status_code = self.response.status_code
