#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import socket
import json

global USERNAME
global PASSWORD
global HOST
global PORT


def set_network_params(host, port):
    HOST = host
    PORT = int(port)


def set_user_params(username, password):
    USERNAME = username
    PASSWORD = password


def parse(data):
    return json.loads(data.decode('utf8'))


def status():
    return parse(send_request({'action': 'status'}))


def join_game():
    send_request({'action': 'join'})


def create_game(rounds=1, players_count=2):
    rounds = int(rounds)
    players_count = int(players_count)
    send_request(dict(action='create_game', players_count=players_count, round_count=rounds))


def make_move(value):
    return parse(send_request({'action': 'make_move', 'move': value}))


def send_request(data):
    request = {
        'username': USERNAME,
        'password': PASSWORD,
    }
    request.update(data)
    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.send(json.dumps(request).encode())
    recv_data = sock.recv(1024 * 8)
    return recv_data


if __name__ == '__main__':
    commands = {
        'set_network_params': set_network_params,
        'set_user_params': set_user_params,
        'status': status,
        'join': join_game,
        'create_game': create_game,
        'make_move': make_move,
    }
    HOST = '127.0.0.1'
    PORT = 1488

    if os.path.isfile('./player.json'):
        with open('./player.json') as f:
            json_file = json.loads(f.read())
        USERNAME = json_file['username']
        PASSWORD = json_file['password']
    else:
        print('To start play you must register user')
        username = input('Username: ')
        password = input('Password: ')
        USERNAME = username
        PASSWORD = password
        with open('./player.json', 'w') as f:
            f.write(json.dumps({'username': username, 'password': password}))
    print('Hello %s' % USERNAME)

    game_status = status()
    print(game_status)

    if game_status['status'] == 'ok':
        if game_status['is_exists'] is False:
            create_game(1, 2)

    join_game()

    moves = {1: 'rock', 2: 'paper', 3: 'scissors'}
    move = input('Make your move! (1 - rock, 2 - paper, 3 - scissors): ')
    print(make_move(moves[int(move)]))
