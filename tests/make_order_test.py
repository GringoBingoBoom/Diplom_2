import allure
import urls
from api import ApiRequest
from data import MessagesResponse
from helpers import CreatePayload


class TestMakeOrder:

    @allure.title('4.1. Создание заказа: с авторизацией')
    def test_make_order_with_autorization(self, payload, create_user):
        """
        создаем нового пользователя и делаем заказ с токеном c первым ингредиентом из списка
        """
        payload_token = CreatePayload.payload_authorization(create_user.json()['accessToken'])
        ingredient = ApiRequest.get(urls.INGREDIENTS, None).json()['data'][0]['_id']
        payload_ingredient = CreatePayload.payload_ingredient(ingredient)
        response = ApiRequest.post_with_token(urls.ORDER, payload_token, payload_ingredient)
        r = response.json()

        assert r['success'] and response.status_code == 200, \
            f'не удалось сделать заказ {r['success']=} и {response.status_code=}'

    @allure.title('4.2. Создание заказа: без авторизации')
    def test_make_order_without_autorization(self, payload):
        """
        делаем заказ без токена c первым ингредиентом из списка
        """
        ingredient = ApiRequest.get(urls.INGREDIENTS, None).json()['data'][0]['_id']
        payload_ingredient = CreatePayload.payload_ingredient(ingredient)
        response = ApiRequest.post(urls.ORDER, payload_ingredient)
        r = response.json()

        assert r['success'] and response.status_code == 200, \
            f'не удалось сделать заказ {r['success']=} и {response.status_code=}'

    @allure.title('4.3. Создание заказа: без ингредиентов')
    def test_make_order_without_ingredient(self, payload, create_user):
        """
        создаем нового пользователя и делаем заказ с токеном без ингредиентов
        """
        payload_token = CreatePayload.payload_authorization(create_user.json()['accessToken'])
        ingredient = []
        payload_ingredient = CreatePayload.payload_ingredient(ingredient)
        response = ApiRequest.post_with_token(urls.ORDER, payload_token, payload_ingredient)
        r = response.json()

        assert r['message'] == MessagesResponse.NO_INGREDIENT and response.status_code == 400

    @allure.title('4.4. Создание заказа: с неверным хешем ингредиентов')
    def test_make_order_wrong_hash_ingredient(self, payload, create_user):
        """
        создаем нового пользователя и делаем заказ с неверным хешем ингредиентов
        """
        payload_token = CreatePayload.payload_authorization(create_user.json()['accessToken'])
        ingredient = ['wrong_hash_ingredient']
        payload_ingredient = CreatePayload.payload_ingredient(ingredient)
        response = ApiRequest.post_with_token(urls.ORDER, payload_token, payload_ingredient)

        assert response.status_code == 500

