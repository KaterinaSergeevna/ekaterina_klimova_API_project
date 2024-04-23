import requests
from endpoints.base_endpoints import BaseEndpoint
from endpoints.json_schemas import DataModel

HEADERS = {
    'Content-type': 'application/json'
}
PUT_PAYLOAD = {
    "name": "MY_Apple MacBook Pro 16100",
    "data": {
        "year": 2014,
        "price": 4849.99,
        "CPU model": "Intel Core i9",
        "Hard disk size": "120 TB"
    }
}


class PutObject(BaseEndpoint):

    def send_put_request(self, post_id, put_payload=None, headers=None):
        headers = headers if headers else HEADERS
        put_payload = put_payload if put_payload else PUT_PAYLOAD
        self.response = requests.put(f"http://167.172.172.115:52355/meme/{post_id}", json=put_payload,
                                     headers={"Authorization": self.token})
        self.status_code = self.response.status_code
        self.response_json = self.response.json()
