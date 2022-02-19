#!/usr/bin/env python3

import socket as soc

HOST = '127.0.0.1'
PORT = 800

with soc.socket(soc.AF_INET, soc.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    s.sendall(b'hello, world')
    data = s.recv(1024)
    
print('recieved', repr(data))

