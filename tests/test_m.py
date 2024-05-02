import allure
from tests.base_test import BaseTest
import pytest


class TestApi(BaseTest):
    data = {
        "text": "example for test",
        "url": "http://tratatata",
        "tags": ["lala", "just for fun"],
        "info": {"colors": ["blue"], "range": 9}
    }

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

    # DELETE /meme/<id>
    # Проверить что мем удалился и статуса ответа 200, статуса ответа 404 при запросе на удаленный ид
    # Проверка удаления с  несуществующим ИД
    # Проверить, что только авторизованные пользователи имеют доступ
    # Проверить, что нельзя удалить чужой мем
    @allure.feature('DELETE /meme/<id>')
    @allure.story('Delete and check that meme was deleted')
    def test_check_that_meme_is_deleted(self, token):
        p_id = self.post_ends.create_meme(token, payload=self.data)
        self.delete_ends.delete_meme(p_id, token)
        self.delete_ends.check_status_is_200()
        self.get_ends.get_meme_by_id(p_id, token)
        self.get_ends.check_status_code_is_404()

    @allure.feature('DELETE /meme/<id>')
    @allure.story('Try to delete meme with unreal id')
    def test_check_deletion_meme_with_unreal_id(self, token):
        self.delete_ends.delete_meme_with_unreal_id(token)
        self.delete_ends.check_status_code_is_404()

    @allure.feature('DELETE /meme/<id>')
    @allure.story('Try to delete meme without authorization')
    def test_check_deletion_meme_without_token(self, token):
        p_id = self.post_ends.create_meme(token, payload=self.data)
        self.delete_ends.delete_without_token(p_id)
        self.delete_ends.check_status_code_is_401()

    @allure.feature('DELETE /meme/<id>')
    @allure.story('Try to delete other meme')
    def test_check_that_other_meme_not_deleted(self, token, p_id=2):
        self.delete_ends.delete_meme(token, p_id)
        self.delete_ends.check_status_code_is_403()

    @allure.feature('DELETE /meme/<id>')
    @allure.story('Try to delete all memes')
    def test_check_that_all_memes_not_deleted(self, token):
        self.delete_ends.delete_all_memes(token)
        self.delete_ends.check_status_code_is_405()
