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

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.HOST, self.PORT))
        self.socket.listen()
        print("Server has started on IP: " + str(host) + " and port: " + str(port))

    def __del__(self):
        self.disconnect()

    def connect(self):
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
                else:
                    self.clients.append(temp)
                    self.numClients = len(self.clients)
                    print("Connecting to a client...")
                    _thread.start_new_thread(self._listenClient, (clientsocket,))
                    print("Connected to the " + str(self.numClients) + " client at: " + str(clientsocket.gethostbyname(clientsocket.gethostname())))
            except:
                raise Exception("Failed to establish new connection!")

    def disconnect(self):
        print("Server closing down...")
        self.RUN = False
        sleep(1)
        self.socket.close()

    def updateCommends(self, commend):
        self.commendsQueue.put(commend)

    def createCommends(self):
        commend = str(random.randint(1, 4) * 4)
        self.commendsQueue.put(commend)

    def _listenRobot(self, robot):
        while self.RUN:
            if self.commendsQueue.qsize() <= 0:
                self.createCommends()

            qsize = self.commendsQueue.qsize()
            for i in range(qsize):
                robot.sendall(pickle.dumps(self.commendsQueue.get()))

        robot.sendall(pickle.dumps("end"))

    def _listenClient(self, clientsocket):
        while self.RUN:
            self.updateCommends(pickle.loads(clientsocket.socket.recv(4096)))

        clientsocket.sendall(pickle.dumps("end"))
            
if __name__ == "__main__":
    server = Server()
    server.connect()

