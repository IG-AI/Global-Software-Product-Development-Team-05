from queue import Queue
import socket, pickle

class Client:
    def __init__(self, host='127.0.1.1', port=2627):
        self.SERVER_HOST = host
        self.SERVER_PORT = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1)
        self.commendsQueue = Queue()

    def __del__(self):
        self.socket.close()

    def connect(self):
        run = True
        with self.socket as socket:
            try:
                print(
                    "Connecting to server on IP: " + str(self.SERVER_HOST) + " and port: " + str(self.SERVER_PORT))
                socket.connect((self.SERVER_HOST, self.SERVER_PORT))
                socket.sendall(pickle.dumps('client'))
            except:
                raise Exception("The client couldn't connect to the server!")

            print("Starts executing client...")
            while run:
                try:
                    data = pickle.loads(self.socket.recv(4096))
                    if data == "end":
                        print("client disconnecting...")
                        run = False
                        self.disconnect()
                        self.socket.close()
                except:
                    pass
                try:
                    if self.commendsQueue.qsize() > 0:
                        socket.sendall(pickle.dumps(self.commendsQueue.get()))
                except:
                    pass

    def disconnect(self):
        self.socket.close()

    def setCommends(self, commend):
        self.commendsQueue.put(commend)

if __name__ == "__main__":
    client = Client()
    client.connect()