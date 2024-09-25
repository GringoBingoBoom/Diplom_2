import allure
import requests
import urls


class ApiRequest:
    # метод запроса POST возвращает список из логина, пароля, кода ответа и текст
    @staticmethod
    @allure.step('API запрос POST по BASE_URL+api_url')
    def post(api_url: str, payload: dict):
        # отправляем запрос post
        return requests.post(urls.BASE_URL + api_url, json=payload)

    @staticmethod
    @allure.step('API запрос GET по BASE_URL+api_url')
    def get(api_url: str, payload: dict = None):
        # отправляем запрос get
        if payload:
            return requests.get(urls.BASE_URL + api_url, json=payload)
        else:
            return requests.get(urls.BASE_URL + api_url)

    @staticmethod
    @allure.step('API запрос DELETE по BASE_URL+api_url')
    def delete(api_url: str, payload_token: dict):
        # отправляем запрос delete
        return requests.delete(urls.BASE_URL + api_url, headers=payload_token)

    @staticmethod
    @allure.step('API запрос PATCH по BASE_URL+api_url')
    def patch(api_url: str, payload_token: dict, payload: dict):
        # отправляем запрос patch
        return requests.patch(urls.BASE_URL + api_url, headers=payload_token, json=payload)

    @staticmethod
    @allure.step('API запрос POST по BASE_URL+api_url')
    def post_with_token(api_url: str, payload_token: dict, payload: dict):
        # отправляем запрос post with token
        return requests.post(urls.BASE_URL + api_url, headers=payload_token, json=payload)

    @staticmethod
    @allure.step('API запрос POST по BASE_URL+api_url')
    def post_logout(api_url: str):
        # отправляем запрос post
        return requests.post(urls.BASE_URL + api_url)

    @staticmethod
    @allure.step('API запрос GET по BASE_URL+api_url')
    def get_with_token(api_url: str, payload_token: dict):
        # отправляем запрос get with token
        return requests.get(urls.BASE_URL + api_url, headers=payload_token)
