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


def status():
    send_request({'action': 'status'})


def join_game():
    send_request({'action': 'join'})


def create_game(rounds=1, players_count=2):
    rounds = int(rounds)
    players_count = int(players_count)
    send_request(dict(action='create_game', players_count=players_count, round_count=rounds))


def make_move(value):
    send_request({'action': 'make_move', 'move': value})


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
    print(recv_data)


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
    USERNAME = 'test'
    PASSWORD = 'test'
    while True:
        cmd = input('Input command' + os.linesep)
        cmd = cmd.split(' ')
        command = commands.get(cmd[0])
        if command is not None:
            command(*cmd[1:])
