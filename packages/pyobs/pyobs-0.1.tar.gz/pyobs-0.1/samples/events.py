#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time

import logging
logging.basicConfig(level=logging.INFO)

sys.path.append('../')
from pyobs import Client, events

host = "localhost"
port = 4444
password = "secret"


def on_event(message):
    print("Got message: {}".format(message))


def on_switch(message):
    print("You changed the scene to {}".format(message.getSceneName()))


ws = Client(host, port, password)
ws.register(on_event)
ws.register(on_switch, events.SwitchScenes)
ws.connect()

try:
    print("OK")
    time.sleep(10)
    print("END")

except KeyboardInterrupt:
    pass

ws.disconnect()
