#!/usr/bin/env python3

import socket as soc
from protocol import htcpcpMessage

HOST = 'raspberrypi.local'
PORT = 80

def Request(method, body = None):
    with soc.socket(soc.AF_INET, soc.SOCK_STREAM) as s:
        s.connect((HOST,PORT))
        request = htcpcpMessage.HtcpcpRequest()
        request.method = method
        request.setUri("English", HOST, pot = 0)
        request.body = body
        s.sendall(bytes(request.create(), "utf-8"));
        response = htcpcpMessage.HtcpcpResponse.fromFile(s.makefile())
        print(response.create())


