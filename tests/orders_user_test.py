import allure
import urls
from api import ApiRequest
from data import MessagesResponse
from helpers import CreatePayload


class TestOrdersUser:

    @allure.title('setup')
    def setup_method(self):
        self.teardown_payload = None

    @allure.title('5.1. Получение заказов конкретного пользователя: авторизованный пользователь')
    def test_get_ordes_authorized_user(self, payload, create_user, make_order):
        """
        создаем пользователя, заказ и делаем запрос на список заказов с токеном
        """
        self.teardown_payload = payload
        payload_token = make_order[1]
        response = ApiRequest.get_with_token(urls.ORDER, payload_token)
        r = response.json()
        response_ingredient_id = r['orders'][0]['_id']
        expected_ingredient_id = make_order[0].json()['order']['_id']

        assert response_ingredient_id == expected_ingredient_id and response.status_code == 200

    @allure.title('5.2. Получение заказов конкретного пользователя: неавторизованный пользователь')
    def test_get_ordes_unauthorized_user(self, payload, create_user, make_order):
        """
        создаем пользователя, заказ и делаем запрос на список заказов без токена
        """
        self.teardown_payload = payload
        payload_token = CreatePayload.payload_authorization('Empty_token')  # неавторизованный пользователь
        response = ApiRequest.get_with_token(urls.ORDER, payload_token)
        r = response.json()

        assert r['message'] == MessagesResponse.should_be_authorised and response.status_code == 401

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


