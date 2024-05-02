import logging
import allure

logging.getLogger(__name__)
logging.basicConfig(level=logging.info('msg'))


class BaseEndpoint:
    response = None
    status_code = None
    response_json = None

    data = {
        "text": "example for test",
        "url": "http://tratatata",
        "tags": ["lala", "just for fun"],
        "info": {"colors": ["blue"], "range": 9}
    }

    @allure.step('Check status code is 200')
    def check_status_is_200(self):
        assert self.status_code == 200


    @allure.step('Check status code is 400')
    def check_status_code_is_400(self):
        logging.info(f'status code for method \'check_status_code_is_400\' is {self.status_code}')
        assert self.status_code == 400

    @allure.step('Check status code is 401')
    def check_status_code_is_401(self):
        logging.info(f'status code for method \'check_status_code_is_401\' is {self.status_code}')
        assert self.status_code == 401

    @allure.step('Check status code is 403')
    def check_status_code_is_403(self):
        logging.info(f'status code for method \'check_status_code_is_403\' is {self.status_code}')
        assert self.status_code == 403

    @allure.step('Check status code is 404')
    def check_status_code_is_404(self):
        logging.info(f'status code for method \'check_status_code_is_404\' is {self.status_code}')
        assert self.status_code == 404

    @allure.step('Check status code is 405')
    def check_status_code_is_405(self):
        logging.info(f'status code for method \'check_status_code_is_405\' is {self.status_code}')
        assert self.status_code == 405
