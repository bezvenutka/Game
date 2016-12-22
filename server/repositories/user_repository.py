import hashlib

from .generic_repository import GenericRepository
from .exceptions import UserAlreadyExistsError


class UserRepository(GenericRepository):
    table_info = ('users', 'username TEXT, password TEXT, score INTEGER')

    def create_user(self, username, password):
        if self.is_user_exist(username) is True:
            raise UserAlreadyExistsError
        query = 'INSERT INTO users VALUES(?, ?, 0)'
        self.exec_query(query, (username, hashlib.sha256(password.encode()).hexdigest()))

    def is_user_exist(self, username):
        query = 'SELECT * FROM users WHERE username=?'
        result = self.exec_query(query, [username])
        if len(result):
            return True
        return False

    def is_password_correct(self, username, password):
        query = 'SELECT * FROM users WHERE username=? AND password=?'
        result = self.exec_query(query, [username, hashlib.sha256(password.encode()).hexdigest()])
        if len(result):
            return True
        return False
