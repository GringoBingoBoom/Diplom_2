import allure
import urls
from api import ApiRequest
from data import MessagesResponse
from helpers import CreatePayload


class TestOrdersUser:

    @allure.title('5.1. Получение заказов конкретного пользователя: авторизованный пользователь')
    def test_get_orders_authorized_user(self, payload, create_user, make_order):
        """
        создаем пользователя, заказ и делаем запрос на список заказов с токеном
        """
        payload_token = make_order[1]
        response = ApiRequest.get_with_token(urls.ORDER, payload_token)
        r = response.json()
        response_ingredient_id = r['orders'][0]['_id']
        expected_ingredient_id = make_order[0].json()['order']['_id']

        assert response_ingredient_id == expected_ingredient_id and response.status_code == 200

    @allure.title('5.2. Получение заказов конкретного пользователя: неавторизованный пользователь')
    def test_get_orders_unauthorized_user(self, payload, create_user, make_order):
        """
        создаем пользователя, заказ и делаем запрос на список заказов без токена
        """
        payload_token = CreatePayload.payload_authorization('Empty_token')  # неавторизованный пользователь
        response = ApiRequest.get_with_token(urls.ORDER, payload_token)
        r = response.json()

        assert r['message'] == MessagesResponse.SHOULD_BE_AUTHORISED and response.status_code == 401




