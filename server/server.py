import socket as soc

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
                data = conn.recv(1024)
                if not data:
                    break
                print("Client Says: " + data.decode("utf-8"))
                conn.sendall(b"Server says: Hi!")
            except soc.error:
                print("An error occured")
                break 
