import allure
import urls
from api import ApiRequest
from data import MessagesResponse
from helpers import CreatePayload


class TestMakeOrder:

    @allure.title('setup')
    def setup_method(self):
        self.teardown_payload = None

    @allure.title('4.1. Создание заказа: с авторизацией')
    def test_make_order_with_autorization(self, payload, create_user):
        """
        создаем нового пользователя и делаем заказ с токеном c первым ингредиентом из списка
        """
        self.teardown_payload = payload
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
        создаем нового пользователя и делаем заказ без токена c первым ингредиентом из списка
        """
        self.teardown_payload = payload
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
        self.teardown_payload = payload
        payload_token = CreatePayload.payload_authorization(create_user.json()['accessToken'])
        ingredient = []
        payload_ingredient = CreatePayload.payload_ingredient(ingredient)
        response = ApiRequest.post_with_token(urls.ORDER, payload_token, payload_ingredient)
        r = response.json()

        assert r['message'] == MessagesResponse.no_ingredient and response.status_code == 400

    @allure.title('4.4. Создание заказа: с неверным хешем ингредиентов')
    def test_make_order_wrong_hash_ingredient(self, payload, create_user):
        """
        создаем нового пользователя и делаем заказ с неверным хешем ингредиентов
        """
        self.teardown_payload = payload
        payload_token = CreatePayload.payload_authorization(create_user.json()['accessToken'])
        ingredient = ['wrong_hash_ingredient']
        payload_ingredient = CreatePayload.payload_ingredient(ingredient)
        response = ApiRequest.post_with_token(urls.ORDER, payload_token, payload_ingredient)

        assert response.status_code == 500

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


