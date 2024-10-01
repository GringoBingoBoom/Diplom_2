import allure
import pytest
import urls
from api import ApiRequest
from data import MessagesResponse
from helpers import CreatePayload


class TestChangeUserData:
    dataset_change_data = [
        {'name': 'name_modified'},
        {'email': 'email_modified'},
        {'password': 'password_modified'}
    ]

    @allure.title('3.1. Изменение данных пользователя: с авторизацией')
    @pytest.mark.parametrize('change_data', dataset_change_data)
    def test_change_user_data_with_autorization(self, payload, create_user, change_data):
        """
        создаем нового пользователя и меняем данные
        """
        r = create_user.json()
        payload_token = CreatePayload.payload_authorization(r['accessToken'])
        response = ApiRequest.patch(urls.USER_INFO, payload_token, change_data)
        r = response.json()
        if r['success']:
            self.teardown_payload = payload | change_data

        assert r['success'] and response.status_code == 200, \
            f'не удалось изменить данные {r['success']=} и {response.status_code=}'

    @allure.title('3.2. Изменение данных пользователя: без авторизации')
    @pytest.mark.parametrize('change_data', dataset_change_data)
    def test_change_user_data_without_autorization(self, payload, create_user, change_data):
        """
        создаем нового пользователя и пробуем менять данные без авторизации
        """
        payload_token = CreatePayload.payload_authorization('Empty_token')  # неавторизованный пользователь
        response = ApiRequest.patch(urls.USER_INFO, payload_token, change_data)
        r = response.json()
        if r['success']:
            self.teardown_payload = payload | change_data

        assert r['message'] == MessagesResponse.SHOULD_BE_AUTHORISED and response.status_code == 401

