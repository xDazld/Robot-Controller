"""
To be run on the computer connected to a controller.
"""

import socket
import json

command_connection = socket.create_connection(('192.168.4.1', 7626))
telemetry_connection = socket.create_connection(('192.168.4.1', 7627))
telemetry = {}
commands = {'Exit': False}


def setup():
    command_connection.send(b'MR Controls 0.1\n')


def loop():
    send_commands()
    read_telemetry()
    print(telemetry)


def send_commands():
    json.dump(commands, command_connection.makefile(mode='rw'))
    command_connection.send(b'\n')


def read_telemetry():
    global telemetry
    telemetry = json.loads(telemetry_connection.makefile(mode='rw').readline())


setup()
while True:
    loop()
