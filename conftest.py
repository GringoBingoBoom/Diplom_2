import pytest
import urls
from api import ApiRequest
from helpers import CreatePayload


@pytest.fixture(scope='function')
def payload():
    return CreatePayload.create_payload()


@pytest.fixture(scope='function')
def create_user(payload):
    user = ApiRequest.post(urls.CREATE_USER, payload)

    yield user

    # teardown
    payload_login = CreatePayload.payload_for_login(payload)
    response = ApiRequest.post(urls.AUTHORIZATION, payload_login)
    if response.status_code == 200:  # если пользователь существует удаляем данные о нем
        r = response.json()
        payload_token = CreatePayload.payload_authorization(r['accessToken'])
        response_del = ApiRequest.delete(urls.USER_INFO, payload_token)
        print(response_del.json(), payload)
        assert response_del.status_code == 202, f'Значение {response_del.status_code=} не равно 202'


@pytest.fixture(scope='function')
def login_user(payload):
    payload_login = CreatePayload.payload_for_login(payload)
    return ApiRequest.post(urls.AUTHORIZATION, payload_login)


@pytest.fixture(scope='function')
def make_order(create_user):
    payload_token = CreatePayload.payload_authorization(create_user.json()['accessToken'])
    ingredient = ApiRequest.get(urls.INGREDIENTS, None).json()['data'][0]['_id']
    payload_ingredient = CreatePayload.payload_ingredient(ingredient)
    return ApiRequest.post_with_token(urls.ORDER, payload_token, payload_ingredient), payload_token
