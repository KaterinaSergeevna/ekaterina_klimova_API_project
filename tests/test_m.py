import allure
from tests.base_test import BaseTest
import pytest


class TestApi(BaseTest):

    # проверить авторизацию с невалидными данными
    @pytest.mark.parametrize("creads", [None, {"name": 1234}, {"name": ["lina", "Jora"]}])
    def test_check_invalid_token_return_text_error(self, creads):
        self.post_ends.take_token_for_other_name(creads)
        self.post_ends.check_status_code_is_400()


    # тест с параметрайзом на проверку типа данных для имени
    # послать пустой запрос

    # Получение списка всех мемов GET /meme

    # Проверить, что только авторизованные пользователи имеют доступ к меме


    # Проверка статус 200
    # Проверить формат возвращаемых данных
    # Проверить что ответ содержит хотябы один мем


    # Проверка с валидным ИД GET / meme / < id >
    def test_get_meme_by_id(self, post_id, token):
        self.get_ends.get_meme_by_id(post_id, token)
        self.get_ends.check_status_is_200()
        self.get_ends.check_that_id_is(post_id)

    # Проверить, что только авторизованные пользователи имеют доступ к меме
    def test_access_without_token_is_impossible(self, post_id):
        self.get_ends.get_meme_by_id_without_token(post_id)
        self.get_ends.check_status_code_is_401()

    # Проверка с невалидным ИД GET / meme / < id >
    def test_get_meme_by_invalid_id(self, token, post_id=123456789):
        self.get_ends.get_meme_by_id(post_id, token)
        self.get_ends.check_status_code_is_404()

    # Проверить, что только авторизованные пользователи имеют доступ к меме POST /meme
    def test_post_meme_without_token(self):
        data = {
            'text': 'example for test',
            'url': 'http://tratatata',
            'tags': ["lala", "just for fun"],
            'info': {"color": "blue", "range": 9}
        }
        self.post_ends.post_meme_without_token(payload=data)
        self.post_ends.check_status_is_401()

    def test_create_meme(self):
        data = {
            "text": "example for test",
            "url": "http://tratatata",
            "tags": ["lala", "just for fun"],
            "info": {"color": "blue", "range": 9}
        }
        self.post_ends.create_meme(payload=data)
        self.post_ends.check_status_is_200()
        self.post_ends.check_data_model()
    # Проверить успешный статус
    # Проверить что мем создался
    # Проверить что данные в ответе соответствуют данным при создании
    # Проверить уникальность ИД
    # Проверить корректность ошибок - неправильные данные не валят сервер
    # Проверить корректность ошибок - незаполненные обязательные поля не валят сервер

    # Проверить, что только авторизованные пользователи имеют доступ к меме PUT / meme / < id >
    # Проверка статуса ответа 200
    # Проверить что после ответа мем с указанным ид был изменен
    # Проверить корректность ошибок - неправильные данные не валят сервер
    # Проверить корректность ошибок - незаполненные обязательные поля не валят сервер
    # Проверить уникальность ИД

    # Проверить что мем удалился DELETE /meme/<id>
    # Проверка статуса ответа 200 при удалении
    # Проверка статуса ответа 404 при запросе на удаленный ид
    # Проверка удаления с  несуществующим ИД
    # Проверить, что только авторизованные пользователи имеют доступ
