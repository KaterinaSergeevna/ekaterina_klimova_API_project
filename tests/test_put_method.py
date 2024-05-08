import allure
from tests.base_test import BaseTest


class TestPutMethod(BaseTest):
    data = {
        "text": "example for test",
        "url": "http://tratatata",
        "tags": ["lala", "just for fun"],
        "info": {"colors": ["blue"], "range": 9}
    }

    # PUT / meme / < id >
    # Проверить, что только авторизованные пользователи имеют доступ к меме
    # Проверка статуса ответа 200 и Проверить что после ответа мем с указанным ид был изменен
    # Проверить корректность ошибок - неправильные данные не валят сервер
    # Проверить корректность ошибок - незаполненные обязательные поля не валят сервер
    # Проверить, что нельзя изменить чужой мем
    @allure.feature('PUT / meme / < id >')
    @allure.story('Try to send put request without authorization')
    def test_put_meme_without_token(self, token):
        p_id = self.post_ends.create_meme(token, payload=self.data)
        self.put_ends.put_meme_without_token(p_id)
        self.put_ends.check_status_code_is_401()

    @allure.feature('PUT / meme / < id >')
    @allure.story('Change meme via put request')
    def test_change_meme_via_put(self, token):
        put_payload = {
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
        new_meme_id = self.post_ends.create_meme(token, payload=self.data)
        self.post_ends.check_status_is_200()
        self.put_ends.send_put_request(new_meme_id, token)
        self.put_ends.check_status_is_200()
        self.get_ends.get_meme_by_id(new_meme_id, token)
        self.get_ends.check_that_request_data_is_equal_response_data(put_payload)
        self.get_ends.check_that_id_is(new_meme_id)

    @allure.feature('PUT / meme / < id >')
    @allure.story('Try to send post request with incorrect data')
    def test_check_put_incorrect_type_data(self, data_list, token):
        p_id = self.post_ends.create_meme(token, payload=self.data)
        for data in data_list:
            data.update({"id": p_id})
            self.put_ends.put_meme_with_incorrect_data(token, p_id, data)
            self.put_ends.check_status_code_is_400()

    @allure.feature('PUT / meme / < id >')
    @allure.story('Try to send post request without required field')
    def test_check_put_data_without_required_field(self, data_without_required_field_list, token):
        p_id = self.post_ends.create_meme(token, payload=self.data)
        for data in data_without_required_field_list:
            data.update({"id": p_id})
            self.put_ends.put_meme_with_incorrect_data(token, p_id, data)
            self.put_ends.check_status_code_is_400()

    @allure.feature('PUT / meme / < id >')
    @allure.story('Try to change other meme via put request')
    def test_change_other_meme_via_put(self, token):
        self.put_ends.send_put_request_to_other_meme(token)
        self.put_ends.check_status_code_is_403()
