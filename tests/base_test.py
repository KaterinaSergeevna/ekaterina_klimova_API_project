from endpoints.post_object import PostObject
from endpoints.put_object import PutObject
from endpoints.delete_object import DeleteObject
from endpoints.get_object import GetObject


class BaseTest:
    token = None

    def setup_method(self):
        self.post_ends = PostObject()
        self.get_ends = GetObject()
        self.delete_ends = DeleteObject()
        self.put_ends = PutObject()
        self.token = self.post_ends.take_token()

    def check_token(self):
        if not self.get_ends.check_token_is_valid(self.token):
            self.token = self.post_ends.take_token()
