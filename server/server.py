import socket as soc
from urllib import response

from protocol.htcpcpMessage import HtcpcpRequest, HtcpcpResponse

HOST = "127.0.0.1"
PORT = 800

with soc.socket(soc.AF_INET, soc.SOCK_STREAM) as s: #Creates a socket object
    s.bind((HOST,PORT))
    s.listen() #Makes this socket a listener
    conn, addr = s.accept() # Blocks and waits for an incoming connection
    with conn:
        print("Connected by", addr)
        while True:
            try:
                request = HtcpcpRequest.fromFile(s.makefile)
                print(request)
                response = HtcpcpResponse()
                response.status = 200
                response.message = "OK"
                
                conn.sendall(bytes(request.create(), "utf-8"))
            except soc.error:
                print("An error occured")
                break 
