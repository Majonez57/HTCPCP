import socket as soc
from htcpcpMessage import HtcpcpRequest, HtcpcpResponse

HOST = 'raspberrypi.local'
PORT = 800

def Request(method, body = None):
    with soc.socket(soc.AF_INET, soc.SOCK_STREAM) as s:
        s.connect((HOST,PORT))
        request = HtcpcpRequest()
        request.method = method
        request.setUri("English", HOST, pot = 0)
        request.body = body
        s.sendall(bytes(request.create(), "utf-8"))
        response = HtcpcpResponse.fromFile(s.makefile())
        print(response.create())


