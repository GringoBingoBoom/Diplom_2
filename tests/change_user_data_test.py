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

    @allure.title('setup')
    def setup_method(self):
        self.teardown_payload = None

    @allure.title('3.1. Изменение данных пользователя: с авторизацией')
    @pytest.mark.parametrize('change_data', dataset_change_data)
    def test_change_user_data_with_autorization(self, payload, create_user, change_data):
        """
        создаем нового пользователя и меняем данные
        """
        self.teardown_payload = payload
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
        self.teardown_payload = payload
        payload_token = CreatePayload.payload_authorization('Empty_token')  # неавторизованный пользователь
        response = ApiRequest.patch(urls.USER_INFO, payload_token, change_data)
        r = response.json()
        if r['success']:
            self.teardown_payload = payload | change_data

        assert r['message'] == MessagesResponse.SHOULD_BE_AUTHORISED and response.status_code == 401

    @allure.title('teardown')
    def teardown_method(self, payload_login):
        """
        удаляем данные на основании payload. Через авторизацию получаем токен
        """
        if self.teardown_payload:
            payload_login = CreatePayload.payload_for_login(self.teardown_payload)
            response = ApiRequest.post(urls.AUTHORIZATION, payload_login)
            if response.status_code == 200:  # если пользователь существует удаляем данные о нем
                r = response.json()
                payload_del = CreatePayload.payload_authorization(r['accessToken'])
                response_del = ApiRequest.delete(urls.USER_INFO, payload_del)
                print(response_del.json(), self.teardown_payload)
                assert response_del.status_code == 202, f'Значение {response_del.status_code=} не равно 202'

