import allure
import pytest
import urls
from api import ApiRequest
from data import MessagesResponse
from helpers import CreatePayload


class TestUserCreation:
    dataset_missed_field = [
        'email',
        'password',
        'name'
    ]

    @allure.title('setup')
    def setup_method(self):
        self.teardown_payload = None

    @allure.title('1.1. Создание пользователя: создать уникального пользователя')
    def test_create_uniq_user_one_user_added(self, payload):
        """
        создаем одного нового пользователя и передаем payload в teardown_payload
        """
        self.teardown_payload = payload
        response = ApiRequest.post(urls.CREATE_USER, payload)
        r = response.json()

        assert r['success'] and response.status_code == 200, \
            f'пользователь не создан {r['success']=} и {response.status_code=}'

    @allure.title('1.2. Создание пользователя: создать пользователя, который уже зарегистрирован')
    def test_create_user_already_exist(self, payload):
        """
        создаем пользователя который уже существует и передаем payload в teardown_payload
        """
        self.teardown_payload = payload
        ApiRequest.post(urls.CREATE_USER, payload)
        response = ApiRequest.post(urls.CREATE_USER, payload)  # повторное создание пользователя
        r = response.json()

        assert r['message'] == MessagesResponse.already_exists and response.status_code == 403, (
            f'пользователь не создан {r['message']=} и {response.status_code=}')

    @allure.title('1.3. Создание пользователя: создать пользователя и не заполнить одно из обязательных полей')
    @pytest.mark.parametrize('missed_field', dataset_missed_field)
    def test_create_user_with_missed_field(self, missed_field, payload):
        """
        создаем пользователя без обязательного поля 3 набора данных 'email', 'password', 'name'
        """
        del payload[missed_field]
        response = ApiRequest.post(urls.CREATE_USER, payload)
        r = response.json()

        assert r['message'] == MessagesResponse.required_fields and response.status_code == 403, (
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
