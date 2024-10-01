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

    @allure.title('1.1. Создание пользователя: создать уникального пользователя')
    def test_create_uniq_user_one_user_added(self, payload, create_user):
        """
        создаем одного нового пользователя
        """
        r = create_user.json()

        assert r['success'] and create_user.status_code == 200, \
            f'пользователь не создан {r['success']=} и {create_user.status_code=}'

    @allure.title('1.2. Создание пользователя: создать пользователя, который уже зарегистрирован')
    def test_create_user_already_exist(self, payload, create_user):
        """
        создаем пользователя который уже существует
        """
        response = ApiRequest.post(urls.CREATE_USER, payload)  # повторное создание пользователя
        r = response.json()

        assert r['message'] == MessagesResponse.ALREADY_EXISTS and response.status_code == 403, (
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

        assert r['message'] == MessagesResponse.REQUIRED_FIELDS and response.status_code == 403, (
            f'пользователь не создан {r['message']=} и {response.status_code=}')

