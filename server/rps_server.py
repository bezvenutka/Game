import socketserver
import threading
import json

from .game import RPSGame
from .repositories.user_repository import UserRepository

game = None


class RPSHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(8192).strip()
        try:
            self.request.sendall(self.process_data(json.loads(data.decode('utf8'))))
        except json.JSONDecodeError:
            self.request.sendall(self.error('Not valid data!!!'))

    def create_game_action(self, data=None):
        global game
        if game is None:
            game = RPSGame(players_count=data.get('players_count', 2),
                                round_count=data.get('round_count', 1))
            return self.status_ok(text='Game successfully created')
        else:
            return self.error('Can`t create game. The game already going.')

    def status_action(self, data=None):
        if game is None:
            return self.status_ok(text='The game does not exist yet.', is_exists=False)
        else:
            if game.is_started is True:
                return self.status_ok(text='Game already going',
                                      is_started=True, is_exists=True)
            else:
                return self.status_ok(text='Game created. You can join it.',
                                      is_started=False, is_exists=True)

    def join_action(self, data=None):
        if game is not None:
            if game.is_started is False:
                game.add_player(data['username'])
                return self.status_ok(text='Successfully joined')
            else:
                return self.error('Game already started')
        else:
            return self.error('Game doesnt exist')

    def make_move_action(self, data=None):
        move = data['move']
        if move not in game.choices:
            return self.error('Not allowed choice')
        game.make_move(data['username'], move)
        return self.status_ok(text='move accepted')

    def game_status_action(self, data=None):
        return self.status_ok(moves=game.moves, winners=game.round_winners)

    def process_data(self, data):
        try:
            self.check_user(data)
            action = data['action']
            actions = {
                'create_game': self.create_game_action,
                'status': self.status_action,
                'join': self.join_action,
                'make_move': self.make_move_action,
                'game_status': self.game_status_action,
            }
            try:
                return actions[action](data)
            except KeyError:
                return self.error('Unknown action')
        except KeyError as e:
            return self.error('Cant find required field %s' % e.args[0])
        except Exception as e:
            return self.error(e.args[0])

    @classmethod
    def error(cls, msg):
        return json.dumps({'error': msg}).encode()

    @classmethod
    def status_ok(cls, **kwargs):
        result = {'status': 'ok'}
        result.update(kwargs)
        return json.dumps(result).encode()

    def check_user(self, data):
        username = data['username']
        password = data['password']
        user_repository = UserRepository()
        if user_repository.is_user_exist(username):
            if user_repository.is_password_correct(username, password):
                return True
            else:
                raise ValueError('Invalid password')
        else:
            user_repository.create_user(username, password)
            return True


class ServerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.host = '127.0.0.1' or kwargs.get('host')
        self.port = 1488 or kwargs.get('port')
        self.server = socketserver.TCPServer((self.host, self.port), RPSHandler)

    def run(self):
        self.server.serve_forever()

    def stop_server(self):
        self.server.server_close()


def start_server(host='127.0.0.1', port=1488):
    server_thread = ServerThread(kwargs={'host': host, 'port': port})
    server_thread.start()
