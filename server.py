from queue import Queue
from time import sleep
import socket, pickle, _thread, random

class Server:
    def __init__(self, host=socket.gethostbyname(socket.gethostname()), port=2526):
        self.RUN = True
        self.HOST = host
        self.PORT = port

        self.clients = []
        self.robots = []
        self.commendsQueue = Queue()
        self.videostream = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.HOST, self.PORT))
        self.socket.listen()

    def __del__(self):
        self.disconnect()

    def connect(self):
        _thread.start_new_thread(self._connect_aux, ())
        return

    def _connect_aux(self):
        print("Server has started on IP: " + str(self.HOST) + " and port: " + str(self.PORT))
        print("Starts listing to clients...")
        while self.RUN:
            clientsocket, address = self.socket.accept()
            try:
                data = pickle.loads(clientsocket.recv(4096))
            except:
                raise Exception("Failed to receive the client type!")
            try:
                if data == 'robot':
                    print("Connecting to a robot at: " + str(address))
                    self.robots.append(data)
                    self.numRobots = len(self.robots)
                    _thread.start_new_thread(self._listenRobot, (clientsocket,address))
                    print("Connected to the robot!")
                elif data == 'client':
                    print("Connecting to a client at: " + str(address))
                    self.clients.append(data)
                    self.numClients = len(self.clients)
                    _thread.start_new_thread(self._listenClient, (clientsocket,address))
                    print("Connected to a client!")
                elif data == 'camera':
                    print("Connecting to the camera at: " + str(address))
                    _thread.start_new_thread(self._listenCamera, (clientsocket,))
                    print("Connected to the camera!")
                else:
                    print("Unknown device trying to connect!")
            except:
                raise Exception("Failed to establish new connection!")

    def disconnect(self):
        print("Server closing down...")
        self.RUN = False
        self.socket.close()

    def _updateCommends(self, commend):
        self.commendsQueue.put(commend)

    def _createCommends(self):
        commend = str(random.randint(1, 4) * 4)
        self.commendsQueue.put(commend)

    def _listenRobot(self, robotsocket, address):
        while self.RUN:
            if self.commendsQueue.qsize() <= 0:
                self._createCommends()

            try:
                robotsocket.settimeout(1)
                data = pickle.loads(robotsocket.recv(4096))
                if data == "end":
                    print("Disconnecting a robot at " + address[0] + "...")
                    return
            except:
                pass

            commend = self.commendsQueue.get()
            for i in range(self.commendsQueue.qsize() + 1):
                try:
                    robotsocket.sendall(pickle.dumps(commend))
                    print("Successfully sent a commend (" + str(commend) + ") to a robot at: " + address[0])
                except:
                    pass

        hostName = robotsocket.gethostbyname(robotsocket.gethostname())
        print("Disconnecting a robot at " + hostName + "...")
        robotsocket.sendall(pickle.dumps("end"))

    def _listenClient(self, clientsocket, address):
        while self.RUN:
            try:
                data = pickle.loads(clientsocket.recv(4096))
                if data == "end":
                    break
                print("Received " + str(data) + " from a client at: " + address[0])
            except:
                pass

        print("Disconnecting a client at " + address[0] + "...")
        clientsocket.sendall(pickle.dumps("end"))

    def _listenCamera(self, camerasocket):
        while self.RUN:
            try:
                self.videostream = pickle.loads(camerasocket.recv(4096))
            except:
                pass

        print("Disconnecting the camera...")
        camerasocket.sendall(pickle.dumps("end"))
            
if __name__ == "__main__":
    server = Server()
    server.connect()
    while True:
        try:
            data = None
        except KeyboardInterrupt:
            server.disconnect()



