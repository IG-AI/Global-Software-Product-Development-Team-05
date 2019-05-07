from queue import Queue
from time import sleep
import socket, pickle

class Client:
    def __init__(self, host='127.0.1.1', port=2526):
        self.SERVER_HOST = host
        self.SERVER_PORT = port
        self.RUN = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)
        self.commendsQueue = Queue()

    def __del__(self):
        self.socket.close()

    def connect(self):
        try:
            print("Connecting to server on IP: " + str(self.SERVER_HOST) + " and port: " + str(self.SERVER_PORT))
            self.socket.connect((self.SERVER_HOST, self.SERVER_PORT))
            self.socket.sendall(pickle.dumps('client'))
            self.RUN = True
        except:
            raise Exception("The client couldn't connect to the server!")


    def send(self, commend):
        try:
            self.socket.settimeout(1)
            stop = pickle.loads(self.socket.recv(4096))
            if stop == "end":
                self.RUN = False
                self.disconnect()
                return
        except:
            pass
        try:
            print("Trying to send new commend to server (" + str(commend) + ")...")
            self._setCommend(commend)
            self.socket.sendall(pickle.dumps(self.commendsQueue.get()))
        except:
            print("Couldn't send to server, the server is probably disconnected.")
            self.RUN = False
            self.disconnect()
            return

        print("Successfully sent commend to the server! (" + str(commend) + ")")

    def disconnect(self):
        print("Client disconnecting...")
        try:
            self.socket.sendall(pickle.dumps("end"))
        except:
            pass
        finally:
            self.socket.close()

    def _setCommend(self, commend):
        self.commendsQueue.put(commend)

if __name__ == "__main__":
    client = Client()
    client.connect()
    for i in range(10):
        client.send('1')
        sleep(1)
    client.disconnect()
