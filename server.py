from queue import Queue
from time import sleep
import socket, pickle, _thread, random

class Server:
    """
    A class which acts as a server. It connects and handles data between clients, robots and a camera.

    Methods
    -------
    connect(self)
        Starts the server.
    disconnect(self)
        Stops the server.
    """
    def __init__(self, host=socket.gethostbyname(socket.gethostname()), port=2526):
        """
        Initialize the server class, with a host and port as optional input.

        Parameters
        ----------
        host(='127.0.1.1'): string
            A string with the IP address for which the server should use.
        port(=2526): int
            A port number the server server should use.

        Attributes
        ----------
        RUN: bool
            If the server is running.
        HOST : string
            The servers host address.
        PORT : int
            The servers port number.
        clients : list of strings
            List with the connected clients IP addresses.
        robots : list of strings
            List with the connected robots IP addresses.
        commandsQueuesList : list
            A list with the unique Queues for specific robots with manual commands to the robots.
        videostream : Video Stream
            The video stream from the camera.
        socket : socket
            The server socket.
        """
        self.RUN = True
        self.HOST = host
        self.PORT = port

        self.clients = []
        self.robots = []
        self.commandsQueuesList = []
        self.videostream = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.HOST, self.PORT))
        self.socket.listen()

    def __del__(self):
        """
        Disconnects the server if the server object is removed.
        """
        self.disconnect()

    def connect(self):
        """
        Setting up the connection for the server class, with a new thread.
        """
        _thread.start_new_thread(self._connect_aux, ())
        return

    def getRobots(self):
        """
        Returns the list with connected robots.
        """
        return self.robots

    def getClients(self):
        """
        Returns the list with connected clients.
        """
        return self.clients

    def disconnect(self):
        """
        Closing down the connection for the server class.
        """
        print("Server closing down...")
        self.RUN = False
        self.socket.close()

    def _connect_aux(self):
        """
        Aux function for the connection function, which starts new threads with new incoming connections.

        Attributes
        ----------
        socket: socket
            Socket for the connected component.
        address : string
            IP address for the connected component.
        id : vary (string)
            ID if the connection in the form of a string, which can have either the value of robot, client or camera.

        Raises
        ------
        Exception
            If the server can't receive the id, Exception is raised.
        Exception
            If the id isn't a string containing either robot, client or camera, Exception is raised.
        """
        print("Server has started on IP: " + self.HOST + " and port: " + str(self.PORT))
        print("Starts listing to clients...")
        while self.RUN:
            socket, address = self.socket.accept()
            try:
                id = pickle.loads(socket.recv(4096))
            except:
                raise Exception("Failed to receive the client type!")
            try:
                if id == 'robot':
                    print("Connecting to a robot at: " + str(address))
                    self.robots.append(address)
                    _thread.start_new_thread(self._listenRobot, (socket,address))
                    print("Connected to the robot!")
                elif id == 'client':
                    print("Connecting to a client at: " + str(address))
                    self.clients.append(address)
                    _thread.start_new_thread(self._listenClient, (socket,address))
                    print("Connected to a client!")
                elif id == 'camera':
                    print("Connecting to the camera at: " + str(address))
                    _thread.start_new_thread(self._listenCamera, (socket,))
                    print("Connected to the camera!")
                else:
                    print("Unknown device trying to connect!")
            except:
                raise Exception("Failed to establish new connection!")

    def _updateCommands(self, command):
        """
        Updates the commands queue.

        Parameters
        ----------
        command: string
            The command should be put into the commands queue.
        """
        self.commandsQueue.put(command)

    def _createCommands(self, index):
        """
        Creates commands for the robots, if no client has sent a command.
        """
        command = str(random.randint(1, 4) * 4)
        self.commandsQueuesList[index][1].put(command)

    def _findCommandsQueue(self, address):
        """
        Finds a unique commands queue for a specific robot.

        Parameters
        ----------
        address: string
            The address of the robot you want the commands queue for.
        """
        for i in range(len(self.commandsQueuesList)):
            if self.commandsQueuesList[i][0] == address:
                index = i

        return index

    def _listenRobot(self, robotsocket, address):
        """
        Function for listing to a robot. It continues until either the server is shutting down or the current robot has
        shut down.

        Parameters
        ----------
        robotsocket: socket
            The socket for the incoming robot connection.
        address: Tuple of string and int
            A tuple with the IP address of the robot in the form of a string and a port number to the robot in the form
            of a int.
        """
        newQueue = (address, Queue())
        self.commandsQueuesList.append(newQueue)
        while self.RUN:
            index = self._findCommandsQueue(address)

            if self.commandsQueuesList[index][1].qsize() <= 0:
                self._createCommands(index)

            try:
                robotsocket.settimeout(1)
                data = pickle.loads(robotsocket.recv(4096))
                if data == "end":
                    index = self._findCommandsQueue(address)
                    self.commandsQueuesList.pop(index)
                    self.robots.remove(address)
                    print("Disconnecting a robot at " + str(address) + "...")
                    return
            except:
                pass

            index = self._findCommandsQueue(address)
            for i in range(self.commandsQueuesList[index][1].qsize()):
                command = self.commandsQueuesList[index][1].get()
                try:
                    robotsocket.sendall(pickle.dumps(command))
                    print("Successfully sent a command (" + str(command) + ") to a robot at: " + str(address))
                except:
                    pass

        index = self._findCommandsQueue(address)
        self.commandsQueuesList[index].pop()
        self.robots.remove(address)
        hostName = robotsocket.gethostbyname(robotsocket.gethostname())
        print("Disconnecting a robot at " + hostName + "...")
        robotsocket.sendall(pickle.dumps("end"))

    def _listenClient(self, clientsocket, address):
        """
        Function for listing to a client. It continues until either the server is shutting down or the current client
        has shut down.

        Parameters
        ----------
        clientsocket: socket
            The socket for the incoming client connection.
        address: Tuple of string and int
            A tuple with the IP address of the client in the form of a string and a port number to the client in the
            form of a int.
        """
        while self.RUN:
            device, command = pickle.loads(clientsocket.recv(4096))
            if command == "end":
                break
            elif command == "robotlist":
                try:
                    print("Trying to send the robots list to " + str(address))
                    clientsocket.sendall(pickle.dumps(self.getRobots()))
                    print("Successfully sent the robot list to: " + str(address))
                except:
                    print("Failed to send robots list to: " + str(address))
            else:
                for i in range(len(self.commandsQueuesList)):
                    if self.commandsQueuesList[i][0] == device:
                        self.commandsQueuesList[i][1].put(command)
                        print("Received " + str(command) + " to robot at " + str(device) + " from a client at: " + str(address))

        self.clients.remove(address)
        print("Disconnecting a client at " + str(address) + "...")
        clientsocket.sendall(pickle.dumps("end"))

    def _listenCamera(self, camerasocket):
        """
        Function for listing to the camera. It continues until either the server is shutting down or the camera has
        shut down.

        Parameters
        ----------
        camerasocket: socket
            The socket for the incoming camera connection.
        address: Tuple of string and int
            A tuple with the IP address of the camera in the form of a string and a port number to the camera in the
            form of a int.
        """
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