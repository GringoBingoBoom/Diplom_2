import allure
import pytest
import urls
from api import ApiRequest
from data import MessagesResponse
from helpers import CreatePayload


class TestLoginExist:
    dataset_wrong_login = [
        'email',
        'password'
    ]

    @allure.title('setup')
    def setup_method(self):
        self.teardown_payload = None

    @allure.title('2.1. Логин пользователя: логин под существующим пользователем')
    def test_login_exist_user_one_user(self, payload, create_user):
        """
        создаем нового пользователя и успешно логинимся под ним
        """
        self.teardown_payload = payload
        payload_login = CreatePayload.payload_for_login(payload)
        response = ApiRequest.post(urls.AUTHORIZATION, payload_login)
        r = response.json()

        assert r['success'] and response.status_code == 200, \
            f'не удалось авторизоваться {r['success']=} и {response.status_code=}'

    @allure.title('2.2. Логин пользователя: логин с неверным логином и паролем')
    @pytest.mark.parametrize('wrong_field', dataset_wrong_login)
    def test_login_with_missed_field(self, wrong_field, payload):
        """
        создаем нового пользователя и неуспешно логинимся под ним пробуем неверный 'email' или 'password'
        """
        self.teardown_payload = payload
        payload_login = CreatePayload.payload_for_login(payload)
        payload_login[wrong_field] = payload_login[wrong_field] + "corrupt"
        response = ApiRequest.post(urls.AUTHORIZATION, payload_login)
        r = response.json()
        assert r['message'] == MessagesResponse.incorrect_field and response.status_code == 401, (
            f'пользователь не создан {r['message']=} и {response.status_code=}')

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
                payload_token = CreatePayload.payload_authorization(r['accessToken'])
                response_del = ApiRequest.delete(urls.USER_INFO, payload_token)
                print(response_del.json(), self.teardown_payload)
                assert response_del.status_code == 202, f'Значение {response_del.status_code=} не равно 202'

