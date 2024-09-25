FAKE_CEED = 2128506  # ceed для faker


class MessagesResponse:
    """
    ожидаемые ответы на запросы
    """
    already_exists = 'User already exists'
    required_fields = 'Email, password and name are required fields'
    incorrect_field = 'email or password are incorrect'
    should_be_authorised = "You should be authorised"
    no_ingredient = "Ingredient ids must be provided"
