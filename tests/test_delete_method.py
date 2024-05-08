import allure
from tests.base_test import BaseTest


class TestDeleteMethod(BaseTest):
    data = {
        "text": "example for test",
        "url": "http://tratatata",
        "tags": ["lala", "just for fun"],
        "info": {"colors": ["blue"], "range": 9}
    }

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
