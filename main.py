#! /usr/bin/env python
import argparse
import asyncore
import sys

from server import GameServerConnector
from client import RPSClient

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--client', action='store_true', dest='client', help='client mode')
    parser.add_argument('--server', action='store_true', dest='server', help='server mode')
    args = parser.parse_args(sys.argv[1:])

    if args.client is True:
        client = RPSClient('127.0.0.1', 8888, 'hello'.encode())
        asyncore.loop()

    if args.server is True:
        server = GameServerConnector('127.0.0.1', 8888)
        asyncore.loop()
