class UserAlreadyExistsError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = 'Такой пользователь уже существует'
