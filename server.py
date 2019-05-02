from queue import Queue
from time import sleep
import socket, pickle, _thread, random

class Server:
    def __init__(self, host=socket.gethostbyname(socket.gethostname()), port=2627):
        self.RUN = True
        self.HOST = host
        self.PORT = port

        self.clients = []
        self.numClients = len(self.clients)
        self.commendsQueue = Queue()
        self.videostream = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.HOST, self.PORT))
        self.socket.listen()

    def __del__(self):
        self.disconnect()

    def connect(self):
        print("Server has started on IP: " + str(self.HOST) + " and port: " + str(self.PORT))
        print("Starts listing to clients...")
        while self.RUN:
            clientsocket, address = self.socket.accept()
            try:
                temp = pickle.loads(clientsocket.recv(4096))
            except:
                raise Exception("Failed to receive the client type!")
            try:
                if temp == 'robot':
                    print("Connecting to the robot...")
                    _thread.start_new_thread(self._listenRobot, (clientsocket,))
                    print("Connected to the robot!")
                elif temp == 'client':
                    self.clients.append(temp)
                    self.numClients = len(self.clients)
                    print("Connecting to a client...")
                    _thread.start_new_thread(self._listenClient, (clientsocket,))
                    print("Connected to the " + str(self.numClients) + " client at: " + str(address))
                elif temp == 'camera':
                    print("Connecting to the camera...")
                    _thread.start_new_thread(self._listenCamera, (clientsocket,))
                    print("Connected to the camera!")
                else:
                    print("Unknown device trying to connect!")
            except:
                raise Exception("Failed to establish new connection!")

    def disconnect(self):
        print("Server closing down...")
        self.RUN = False
        sleep(1)
        self.socket.close()

    def _updateCommends(self, commend):
        self.commendsQueue.put(commend)

    def _createCommends(self):
        commend = str(random.randint(1, 4) * 4)
        self.commendsQueue.put(commend)

    def _listenRobot(self, robotsocket):
        while self.RUN:
            if self.commendsQueue.qsize() <= 0:
                self._createCommends()

            for i in range(self.commendsQueue.qsize()):
                robotsocket.sendall(pickle.dumps(self.commendsQueue.get()))

        robotsocket.sendall(pickle.dumps("end"))

    def _listenClient(self, clientsocket):
        while self.RUN:
            self._updateCommends(pickle.loads(clientsocket.recv(4096)))

        clientsocket.sendall(pickle.dumps("end"))

    def _listenCamera(self, camerasocket):
        while self.RUN:
            self.videostream = pickle.loads(camerasocket.recv(4096))

        camerasocket.sendall(pickle.dumps("end"))
            
if __name__ == "__main__":
    server = Server()
    server.connect()

