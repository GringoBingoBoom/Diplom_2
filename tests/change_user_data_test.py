import allure
import pytest
import urls
from api import ApiRequest
from data import MessagesResponse
from helpers import CreatePayload


class TestChangeUserData:
    dataset_change_data = [
        {'name': 'name_modified1'},
        {'email': 'email_modified1'},
        {'password': 'password_modified1'}
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

        # добавил teardown в тест т.к. не придумал как по-другому удалять юзера после изменений
        payload_login = CreatePayload.payload_for_login(payload | change_data)
        response_teardown = ApiRequest.post(urls.AUTHORIZATION, payload_login)
        if response_teardown.status_code == 200:  # если пользователь существует удаляем данные о нем
            r_teardown = response_teardown.json()
            payload_token = CreatePayload.payload_authorization(r_teardown['accessToken'])
            ApiRequest.delete(urls.USER_INFO, payload_token)

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

