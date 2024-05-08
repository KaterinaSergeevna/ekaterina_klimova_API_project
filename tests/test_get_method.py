import allure
from tests.base_test import BaseTest
import pytest


class TestGetMethod(BaseTest):

    # GET /authorize/<token>
    # проверить успешное получение токена
    # тест с параметрайзом на проверку типа данных для имени

    @allure.feature('Authorization')
    @allure.story('Take token')
    def test_take_token_is_successfull(self):
        self.post_ends.take_token()
        self.post_ends.check_status_is_200()

    @allure.feature('Authorization')
    @allure.story('check invalid tokens type return 400 error')
    @pytest.mark.parametrize("creads", [None, {"name": 1234}, {"name": ["lina", "Jora"]}])
    def test_check_invalid_tokens_type_return_400_error(self, creads):
        self.post_ends.take_token_for_other_name(creads)
        self.post_ends.check_status_code_is_400()

    # GET /meme
    # Проверка статус 200
    # Проверить, что только авторизованные пользователи имеют доступ к меме
    # Получение списка всех мемов на соответствие формату
    @allure.feature('GET/meme')
    @allure.story('Call all meme endpoint returns 200 status')
    def test_that_meme_endpoints_returns_status_code_200(self, token):
        self.get_ends.get_all_meme(token)
        self.get_ends.check_status_is_200()

    @allure.feature('GET/meme')
    @allure.story('Check that unauthorized user does not have access to meme')
    def test_check_that_unauthorized_user_does_not_have_access_to_meme(self):
        self.get_ends.get_meme_without_token()
        self.get_ends.check_status_code_is_401()

    @allure.feature('GET/meme')
    @allure.story('Check that all memes are correct')
    def test_all_meme_is_correct(self, token):
        self.get_ends.check_that_all_meme_is_correct(token)

    # GET /meme/<id>
    # Проверка с валидным ИД и токеном
    # Проверить, что только авторизованные пользователи имеют доступ к меме по id
    # Проверка с невалидным ключом
    # Проверка с невалидным ИД
    @allure.feature('GET/meme/<id>')
    @allure.story('Get meme by id')
    def test_get_meme_by_id(self, post_id, token):
        self.get_ends.get_meme_by_id(post_id, token)
        self.get_ends.check_status_is_200()
        self.get_ends.check_that_id_is(post_id)

    @allure.feature('GET/meme/<id>')
    @allure.story('Try to get meme without authorization')
    def test_access_without_token_is_impossible(self, post_id):
        self.get_ends.get_meme_by_id_without_token(post_id)
        self.get_ends.check_status_code_is_401()

    @allure.feature('GET/meme/<id>')
    @allure.story('Check that invalid token returns 401 error')
    def test_invalid_token_return_401_error(self, post_id, token="abc"):
        self.get_ends.get_meme_by_id(post_id, token)
        self.get_ends.check_status_code_is_401()

    @allure.feature('GET/meme/<id>')
    @allure.story('Try to get meme by invalid id')
    def test_get_meme_by_invalid_id(self, token, post_id=123456789):
        self.get_ends.get_meme_by_id(post_id, token)
        self.get_ends.check_status_code_is_404()
