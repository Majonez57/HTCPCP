import socket
import io
from htcpcpmessage import HtcpcpResponse, HtcpcpRequest

HOST = 'raspberrypi.local'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    x = HtcpcpRequest()
    x.setUri("English", "localhost", pot = 0)
    x.method = "BREW"
    s.sendall(bytes(x.create()))
    data = HtcpcpResponse(io.StringIO(s.recv(1024)))
    

print('Received', repr(data))