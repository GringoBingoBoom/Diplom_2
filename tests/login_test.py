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

    @allure.title('2.1. Логин пользователя: логин под существующим пользователем')
    def test_login_exist_user_one_user(self, payload, create_user):
        """
        создаем нового пользователя и успешно логинимся под ним
        """
        payload_login = CreatePayload.payload_for_login(payload)
        response = ApiRequest.post(urls.AUTHORIZATION, payload_login)
        r = response.json()

        assert r['success'] and response.status_code == 200, \
            f'не удалось авторизоваться {r['success']=} и {response.status_code=}'

    @allure.title('2.2. Логин пользователя: логин с неверным логином и паролем')
    @pytest.mark.parametrize('wrong_field', dataset_wrong_login)
    def test_login_with_missed_field(self, wrong_field, payload, create_user):
        """
        создаем нового пользователя и неуспешно логинимся под ним пробуем неверный 'email' или 'password'
        """
        payload_login = CreatePayload.payload_for_login(payload)
        payload_login[wrong_field] = payload_login[wrong_field] + "corrupt"
        response = ApiRequest.post(urls.AUTHORIZATION, payload_login)
        r = response.json()
        assert r['message'] == MessagesResponse.INCORRECT_FIELD and response.status_code == 401, (
            f'пользователь не создан {r['message']=} и {response.status_code=}')

