import allure
from tests.base_test import BaseTest


class TestPostMethod(BaseTest):
    data = {
        "text": "example for test",
        "url": "http://tratatata",
        "tags": ["lala", "just for fun"],
        "info": {"colors": ["blue"], "range": 9}
    }

    # POST /meme
    # Проверить, что только авторизованные пользователи имеют доступ
    # Проверить успешный статус после создания, мем создался и находится по ид, переданные данные равны полученным
    # Проверить уникальность ИД для созданного мема
    # Проверить корректность ошибок - неправильные данные не валят сервер
    # Проверить корректность ошибок - незаполненные обязательные поля не валят сервер
    @allure.feature('POST /meme')
    @allure.story('Try to post meme without authorization')
    def test_post_meme_without_token(self):
        self.post_ends.post_meme_without_token(payload=self.data)
        self.post_ends.check_status_code_is_401()

    @allure.feature('POST /meme')
    @allure.story('Create meme')
    def test_create_meme(self, token):
        new_meme_id = self.post_ends.create_meme(token, payload=self.data)
        self.post_ends.check_status_is_200()
        self.get_ends.get_meme_by_id(new_meme_id, token)
        self.get_ends.check_that_request_data_is_equal_response_data(self.data)

    @allure.feature('POST /meme')
    @allure.story('Check that id is unicum for created meme')
    def test_check_that_id_is_unicum(self, token):
        meme_ids = self.get_ends.get_all_id_for_meme(token)
        self.post_ends.create_meme(token)
        self.post_ends.check_status_is_200()
        self.post_ends.check_that_id_is_unicum(meme_ids)

    @allure.feature('POST /meme')
    @allure.story('Test data validation for post method')
    def test_data_validation_for_post_method(self, data_list, token):
        for data in data_list:
            self.post_ends.create_meme(token, payload=data)
            self.post_ends.check_status_code_is_400()

    @allure.feature('POST /meme')
    @allure.story('Try to send post request without required field')
    def test_check_post_data_without_required_field(self, data_without_required_field_list, token):
        for data in data_without_required_field_list:
            self.post_ends.create_meme(token, payload=data)
            self.post_ends.check_status_code_is_400()
