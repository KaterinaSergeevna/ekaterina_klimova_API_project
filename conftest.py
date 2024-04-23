import pytest
from endpoints.post_object import PostObject
from endpoints.delete_object import DeleteObject
from endpoints.get_object import GetObject


@pytest.fixture()
def post_id(create_object):
    create_object.create_meme()
    post_id = create_object.response_json['id']
    yield post_id
    DeleteObject().delete(post_id)


@pytest.fixture()
def token(create_object):
    create_object.take_token()
    token = create_object.response_json["token"]
    return token


@pytest.fixture()
def create_object():
    return PostObject()
