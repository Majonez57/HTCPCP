import socket as soc
from htcpcpMessage import HtcpcpRequest, HtcpcpResponse

HOST = 'raspberrypi.local'
PORT = 8000

def Request(method, body = None):
    with soc.socket(soc.AF_INET, soc.SOCK_STREAM) as s:
        s.connect((HOST,PORT))
        print("Creating request")
        request = HtcpcpRequest()
        request.method = method
        request.setUri("English", HOST, pot = 0)
        request.body = body

        response = HtcpcpResponse.fromFile(s.makefile())
        s.sendall(bytes(request.create(), "utf-8"))
        print(response.create())


