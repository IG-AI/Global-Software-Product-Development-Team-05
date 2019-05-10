from queue import Queue
from time import sleep
import socket, pickle, _thread

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
        self.robotsManualMode = []
        self.robotsStarted = []
        self.videostream = None
        self.map = None

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
        _thread.start_new_thread(self._connectAux, ())
        return

    def _connectAux(self):
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
                    _thread.start_new_thread(self._listenRobot, (socket,address))
                    print("Connected to the robot!")
                elif id == 'client':
                    print("Connecting to a client at: " + str(address))
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

    def setMap(self, map):
        """
        Sets the map over the building the robot(s) should operate in.

        Parameters
        ----------
        map: matrix
            A matrix representing the layout of the building the robot(s) will operate in.
        """
        self.map = map

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

    def startRobot(self, robot, time=None):
        """
        Starts a robot in a new thread

        Parameters
        ----------
        robot: (string, int)
            A tuple with the IP address and port to the robot that should be started.
        time(=None): int
            A optional input, if left the robot will continue until it receives a stop call. Otherwise ot will
            continue equal amout of time as set in the input or until receives a stop call.
        """
        _thread.start_new_thread(self._startRobotAux, (robot, time))

    def _startRobotAux(self, robot, time=None):
        """
        Starts a specific robot as given in the input. A second parameter is optional, if left then the robot continues
        until a stopRobot(robot) has been called. If given as a an int, the robot will run for that amount of time.

        Parameters
        ----------
        robot: (string, int)
            A tuple with the IP address and port to the robot that should be started.
        time(=None): int
            A optional input, if left the robot will continue until it receives a stop call. Otherwise ot will
            continue equal amout of time as set in the input or until receives a stop call.

        Raises
        ------
        Exception
            If input isn't None or an int, Exception is raised.
        """
        if time == None:
            if robot in self.robots:
                print("Starting up robot at: " + str(robot))
                self.robotsStarted.append(robot)
            else:
                print("Robot: " + str(robot) + " isn't connected to the server!")

        elif type(time) == int:
            if robot in self.robots:
                print("Starting up robot at: " + str(robot))
                self.robotsStarted.append(robot)
                sleep(time)
                self.stopRobot(robot)
            else:
                print("Robot: " + str(robot) + " isn't connected to the server!")
        else:
            raise Exception("Invalid input! Input has to be an int.")

    def stopRobot(self, robot):
        """
        Stops a specific robot as given in the input.

        Parameters
        ----------
        robot: (string, int)
            A tuple with the IP address and port to the robot that should be started.
        """
        if robot in self.robotsStarted:
            print("Turning off the robot  at: "+ str(robot))
            self.robotsStarted.remove(robot)
        else:
            print("The robot: " + robot + " hasn't been started!")

    def disconnect(self):
        """
        Closing down the connection for the server class.
        """
        print("Server closing down...")
        self.RUN = False
        sleep(1)
        self.socket.close()

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
        self.robots.append(address)
        sentManualFlag = False
        sentStartFlag = False
        sentAutoFlag = None
        sentStopFlag = None
        while self.RUN:
            sleep(1)
            try:
                robotsocket.settimeout(1)
                data = pickle.loads(robotsocket.recv(4096))
                if data == "end":
                    break
            except:
                pass

            if (address in self.robotsManualMode) & (sentManualFlag == False):
                robotsocket.sendall(pickle.dumps("manual"))
                sentAutoFlag = False
                sentManualFlag = True
            elif (address not in self.robotsManualMode) & (sentAutoFlag == False):
                robotsocket.sendall(pickle.dumps("auto"))
                sentManualFlag = False
                sentAutoFlag = True
            else:
                pass

            if (address in self.robotsStarted) & (sentStartFlag == False):
                robotsocket.sendall(pickle.dumps("start"))
                sentStopFlag = False
                sentStartFlag = True
            elif (address not in self.robotsStarted) & (sentStopFlag == False):
                robotsocket.sendall(pickle.dumps("stop"))
                sentStartFlag = False
                sentStopFlag = True
            else:
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
        self.commandsQueuesList.pop(index)
        try:
            self.robots.remove(address)
        except:
            pass
        try:
            self.robotsManualMode.remove(address)
        except:
            pass
        print("Disconnecting a robot at " + str(address) + "...")
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
        self.clients.append(address)
        while self.RUN:
            sleep(1)
            device, command = pickle.loads(clientsocket.recv(4096))
            if command == "end":
                try:
                    self.clients.remove(address)
                except:
                    pass
                print("Disconnecting a client at " + str(address) + "...")
                return

            elif command == "robotlist":
                try:
                    print("Trying to send the robots list to " + str(address))
                    clientsocket.sendall(pickle.dumps(self.getRobots()))
                    print("Successfully sent the robot list to: " + str(address))
                except:
                    print("Failed to send robots list to: " + str(address))

            elif command == "map":
                print("Trying to send the map to a client at: " + str(address))
                if self.map == None:
                    print("The server hasn't any map!")
                    pass
                elif address in self.clients:
                    clientsocket.sendall(pickle.dumps(self.map))
                    print("Successfully sent the map to a client at: " + str(address))
                else:
                    print("Failed to send robots list to: " + str(address))

            elif command == "manual":
                if device == None:
                    print("Manual Mode Activated for all robots!")
                    for i in range(len(self.robots)):
                        try:
                            self.robotsManualMode.append(self.robots[i])
                        except:
                            pass
                else:
                    print("Manual Mode Activated for a robot at: " + str(device))
                    try:
                        self.robotsManualMode.append(device)
                    except:
                        pass

            elif command == "auto":
                if device == None:
                    print("Auto Mode Activated for all robots!")
                    for i in range(len(self.robots)):
                        try:
                            self.robotsManualMode.remove(self.robots[i])
                        except:
                            pass
                else:
                    print("Auto Mode Activated for a robot at: " + str(device))
                    self.robotsManualMode.remove(device)

            else:
                for i in range(len(self.commandsQueuesList)):
                    if self.commandsQueuesList[i][0] == device:
                        self.commandsQueuesList[i][1].put(command)
                        print("Received " + str(command) + " to robot at " + str(device) + " from a client at: " + str(address))

        try:
            self.clients.remove(address)
        except:
            pass

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
            sleep(1)
            try:
                self.videostream = pickle.loads(camerasocket.recv(4096))
            except:
                pass

        print("Disconnecting the camera...")
        camerasocket.sendall(pickle.dumps("end"))
            
if __name__ == "__main__":
    server = Server()
    server.connect()
    startFlag = False
    startFlag2 = False
    while True:
        sleep(1)
        if (len(server.robots) > 0) & (startFlag == False):
            server.startRobot(server.robots[0], 120)
            startFlag = True
            print("Prutt")

        elif (len(server.robots) > 1) & (startFlag2 == False):
            server.startRobot(server.robots[1], 120)
            startFlag2 = True

