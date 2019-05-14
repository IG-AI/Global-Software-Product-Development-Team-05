import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

while True:
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            #print('Received', repr(data))
            if not data:
                break
            print('Received', repr(data))
            #conn.sendall(data)
        #print('Received', repr(data))
    #print('Received', repr(data))

#print('Received', repr(data))