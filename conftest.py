import pytest
import os
import json
from endpoints.post_object import PostObject
from endpoints.delete_object import DeleteObject
from endpoints.get_object import GetObject


@pytest.fixture()
def post_id(create_object, delete_object, token):
    create_object.create_meme(token)
    post_id = create_object.response_json['id']
    yield post_id
    delete_object.delete_meme(post_id, token)


@pytest.fixture()
def validate_token(get_object, create_object):
    if os.path.getsize('cread.txt') == 0:
        create_object.take_token()
    else:
        with open('cread.txt', 'r') as file:
            token = file.read().strip()
            if not get_object.check_token_is_valid(token):
                create_object.take_token()


@pytest.fixture()
def token(validate_token):
    with open('cread.txt', 'r') as file:
        token = str(file.read().strip())
    return token


@pytest.fixture()
def create_object():
    return PostObject()


@pytest.fixture()
def get_object():
    return GetObject()


@pytest.fixture()
def delete_object():
    return DeleteObject()


@pytest.fixture
def data_list():
    with open("test_data/data_with_incorrect_fields_type.json") as f:
        data = json.load(f)
    return data


@pytest.fixture
def data_without_required_field_list():
    with open("test_data/data_without_required_field.json") as f:
        data = json.load(f)
    return data
