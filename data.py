FAKE_CEED = 212850  # ceed для faker


class MessagesResponse:
    """
    ожидаемые ответы на запросы
    """
    ALREADY_EXISTS = 'User already exists'
    REQUIRED_FIELDS = 'Email, password and name are required fields'
    INCORRECT_FIELD = 'email or password are incorrect'
    SHOULD_BE_AUTHORISED = "You should be authorised"
    NO_INGREDIENT = "Ingredient ids must be provided"
