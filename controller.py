"""
Robot Controller for Midnight Robotics. This should be run on a Raspberry Pi Pico W.
Needs to be saved as main.py on the Microcontroller for it to run on boot.
"""

import network
import sys
import time
import socket
import machine
import json
import io

weapon_power = False
telemetry = {}

print('Starting Controller')

# Set up the network
wlan = network.WLAN(network.AP_IF)
# Get the Wi-Fi name and password from a file named ap_auth.txt stored on the microcontroller.
wlan.config(essid=json.load(io.open('ap_auth.txt'))[0], password=json.load(io.open('ap_auth.txt'))[1])
wlan.active(True)
print('Network Info: ' + str(wlan.ifconfig()))

# Setup server sockets

command_server = socket.socket()
command_server.bind(('', 7626))
command_server.listen()
print('Command Listening')
(command_connection, remote_address) = command_server.accept()

print('Command Connection from ' + str(remote_address))

# Set the unchanging telemetry
telemetry['Reset Cause'] = machine.reset_cause()
telemetry['Implementation'] = json.dumps(sys.implementation)

# Setup server socket
telemetry_server = socket.socket()
telemetry_server.bind(('', 7627))
telemetry_server.listen()
print('Telemetry Listening')
(telemetry_connection, telemetry_address) = telemetry_server.accept()
print('Telemetry Connection from ' + str(telemetry_address))

# wdt = WDT(timeout=8388)  # Watch Dog Timer

# Runs the loop
if command_connection.readline() != b'MR Controls 0.1\n':
    raise Exception
while True:
    # wdt.feed()
    # Get instructions on what to do
    commands = json.loads(command_connection.readline())
    print(commands)
    if commands['Exit']:
        sys.exit()
    # Send back telemetry
    telemetry['Milliseconds'] = time.ticks_ms()
    telemetry_connection.write(json.dumps(telemetry) + '\n')
