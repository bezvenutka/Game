import socket
import asyncore
import json

from .repositories import UserRepository
from .repositories.exceptions import UserAlreadyExistsError


class GameResponseHandler(asyncore.dispatcher_with_send):

    def __init__(self, sock=None, map=None):
        super().__init__(sock, map)
        self.action_table = {
            'register': self.register
        }

    def handle_read(self):
        data = self.recv(8192)
        self.check_message(data)

    def register(self, data):
        if data.get('username') and data.get('password'):
            username = data['username']
            password = data['password']
        else:
            self.send_error('Not enough arguments')
            return

        user_repository = UserRepository()
        try:
            user_repository.new_user(username, password)
        except UserAlreadyExistsError as e:
            self.send_error(e.text)

    def send_error(self, error_text):
        self.send(('{error:{text: "%s"}' % error_text).encode())

    def _parse_data(self, data):
        try:
            json_data = json.loads(data.decode())
        except Exception as e:
            self.send_error(str(e))
            return
        return json_data

    def check_message(self, data):
        json_data = self._parse_data(data)
        if json_data and json_data.get('type'):
            self.action_table[json_data['type']](json_data)
        else:
            self.send_error('No action specified')


class GameServerConnector(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)



    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print('Incoming connection from %s' % repr(addr))
            handler = GameResponseHandler(sock)
