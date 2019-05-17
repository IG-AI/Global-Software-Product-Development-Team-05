import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

def send(HOST, PORT, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(data)
        #data = s.recv(1024)
    #print('Received', repr(data))

if __name__ == "__main__":
    send(HOST, PORT, bytes('hello', 'utf-8'))