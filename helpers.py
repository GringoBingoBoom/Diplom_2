import allure
from faker import Faker
import data

fake = Faker()
fake.seed_instance(data.FAKE_CEED)


class CreatePayload:

    @staticmethod
    @allure.step('Генерируем фейковые данные регистрации нового пользователя')
    def create_payload() -> dict:
        """
        генерируем почту, пароль и имя
        """
        payload = {
            "email": fake.email(),
            "password": fake.password(),
            "name": fake.user_name()
        }

        return payload

    @staticmethod
    @allure.step('Удаляем name из payload')
    def payload_for_login(payload) -> dict:
        """
        удаляем имя
        """
        payload_login = payload.copy()
        del payload_login['name']

        return payload_login

    @staticmethod
    @allure.step('headers для удаления пользователя')
    def payload_authorization(access_token) -> dict:
        """
        формируем header
        """
        payload_authorization = {'Authorization': access_token}

        return payload_authorization

    @staticmethod
    @allure.step('headers для удаления пользователя')
    def payload_ingredient(ingredient) -> dict:
        """
        формируем ingredient
        """
        if type(ingredient) is not list:
            ingredient = [ingredient]
        payload_ingredient = {"ingredients": ingredient}

        return payload_ingredient
