
from queue import Queue
from time import sleep
import socket, pickle, _thread
import util.aiPlacement as ai

class Server:
    """
    A class which acts as a server. It connects and handles data between clients, robots and a camera.
    Methods
    -------
    connect(self):
        Starts the server.
    set_map(self, map):
        Sets the layout map over the area the robots operates in.
    get_robots(self):
        Returns the list with connected robots.
    get_clients(self):
        Returns the list with connected clients.
    start_robot(self, robot, time=None):
        Starts a robot in a new thread, with the duration in seconds as a optional input (time).
    stop_robot(self, robot):
        Stops a specific robot as given in the input.
    disconnect(self):
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
        commands_list : list
            A list with the unique Queues for specific robots with manual commands to the robots.
        videostream : Video Stream
            The video stream from the camera.
        map: Matrix
            A matrix that represent the area the robots operates in.
        sock : socket
            The server sock.
        """
        self.RUN = True
        self.HOST = host
        self.PORT = port

        self.clients = []
        self.robots = []
        self.commands_list = []
        self.robots_manual_mode = []
        self.robots_started = []
        self.videostream = None
        self.map = None
        self.current_layout = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen()

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
        sock: socket
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
            sock, address = self.sock.accept()
            try:
                id = pickle.loads(sock.recv(4096))
            except:
                raise Exception("Failed to receive the client type!")
            try:
                if id == 'robot':
                    print("Connecting to a robot at: " + str(address))
                    _thread.start_new_thread(self._listen_robot, (sock, address))
                    print("Connected to the robot!")
                elif id == 'client':
                    print("Connecting to a client at: " + str(address))
                    _thread.start_new_thread(self._listen_client, (sock, address))
                    print("Connected to a client!")
                elif id == 'camera':
                    print("Connecting to the camera at: " + str(address))
                    _thread.start_new_thread(self._listen_camera, (sock,))
                    print("Connected to the camera!")
                else:
                    print("Unknown device trying to connect!")
            except:
                raise Exception("Failed to establish new connection!")

    def set_map(self, map):
        """
        Sets the map over the building the robot(s) should operate in.
        Parameters
        ----------
        map: matrix
            A matrix representing the layout of the building the robot(s) will operate in.
        """
        self.map = map

    def get_robots(self):
        """
        Returns the list with connected robots.
        """
        return self.robots

    def get_clients(self):
        """
        Returns the list with connected clients.
        """
        return self.clients

    def start_robot(self, robot, time=None):
        """
        Starts a robot in a new thread, with the duration in seconds as a optional input (time).
        Parameters
        ----------
        robot: (string, int)
            A tuple with the IP address and port to the robot that should be started.
        time(=None): int
            A optional input, if left the robot will continue until it receives a stop call. Otherwise ot will
            continue equal amout of time as set in the input or until receives a stop call.
        """
        _thread.start_new_thread(self._start_robot_aux, (robot, time))

    def _start_robot_aux(self, robot, time=None):
        """
        Starts a specific robot as given in the input. A second parameter is optional, if left then the robot continues
        until a stop_robot(robot) has been called. If given as a an int, the robot will run for that amount of time.
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
                print("Starting up robot at: " + str(robot[0]))
                self.robots_started.append(robot[0])
            else:
                print(self.robots)
                print("Robot: " + str(robot[0]) + " isn't connected to the server!")

        elif type(time) == int:
            if robot in self.robots:
                print("Starting up robot at: " + str(robot[0]))
                self.robots_started.append(robot[0])
                sleep(time)
                self.stop_robot(robot)
            else:
                print("Robot: " + str(robot[0]) + " isn't connected to the server!")
        else:
            raise Exception("Invalid input! Input has to be an int.")

    def stop_robot(self, robot):
        """
        Stops a specific robot as given in the input.
        Parameters
        ----------
        robot: (string, int)
            A tuple with the IP address and port to the robot that should be started.
        """
        if robot in self.robots_started:
            print("Turning off the robot  at: "+ str(robot[0]))
            self.robots_started.remove(robot)
        else:
            print("The robot: " + str(robot[0]) + " hasn't been started!")

    def disconnect(self):
        """
        Closing down the connection for the server class.
        """
        print("Server closing down...")
        self.RUN = False
        sleep(1)
        self.sock.close()

    def _find_commands_queue(self, address):
        """
        Finds a unique commands queue for a specific robot.
        Parameters
        ----------
        address: string
            The address of the robot you want the commands queue for.
        """
        for i in range(len(self.commands_list)):
            if self.commands_list[i][0] == address:
                index = i

        return index

    def _find_robot(self, robot):
        """
        Finds a robot in the robot list.
        Parameters
        ----------
        address: string
            The address of the robot you want.
        """
        for i in range(len(self.commands_list)):
            if self.robots[i][0] == robot:
                index = i

        return index

    def _createCommand(self, robot): # - TODO: Create AI
        self.commands_list[len(self.commands_list) - 1][0] = robot
        self.commands_list[len(self.commands_list) - 1][1] = (5, 4) #This should be calculated.

    def _listen_robot(self, robotsocket, address):
        """
        Function for listing to a robot. It continues until either the server is shutting down or the current robot has
        shut down.
        Parameters
        ----------
        robotsocket: socket
            The sock for the incoming robot connection.
        address: Tuple of string and int
            A tuple with the IP address of the robot in the form of a string and a port number to the robot in the form
            of a int.
        """
        newQueue = [address, Queue()]
        self.commands_list.append(newQueue)
        self.robots.append([address, (0,0), "north"])
        sentStartFlag = False
        sentStopFlag = None
        new_grid_layout = ai.init_grid_layout(self.map.height, self.map.width)
        new_grid_layout = ai.init_robot_start_position(new_grid_layout, len(self.robots), (0,0, "north"), self.map.width)
        while self.RUN:
            sleep(1)
            try:
                robotsocket.settimeout(1)
                data = pickle.loads(robotsocket.recv(4096))
                if data == "end":
                    break
            except:
                pass

            try:
                if data[0] == "pos":
                    self.robots[self._find_robot(address)][1] = data[1]


            except:
                pass

            if (address in self.robots_started) & (sentStartFlag == False):
                robotsocket.sendall(pickle.dumps("start"))
                sentStopFlag = False
                sentStartFlag = True
            elif (address not in self.robots_started) & (sentStopFlag == False):
                robotsocket.sendall(pickle.dumps("stop"))
                sentStartFlag = False
                sentStopFlag = True
            else:
                pass

            index = self._find_commands_queue(address)

            print("Test: " + str(self.commands_list))
            if self.commands_list[index][1].empty():
                self._createCommand(address)

            command = self.commands_list[index].pop(1)
            print(new_grid_layout)
            direction, robotNextPosition, new_grid_layout, goalPosition = ai.next_action_and_position_and_grid_update(self.map.width, self.map.height, new_grid_layout, command[1], command[0], len(self.robots))
            X, Y, direction = robotNextPosition
            self.current_layout = new_grid_layout
            self.robots[self._find_robot(address)][1] = (X, Y)
            self.robots[self._find_robot(address)][2] = direction
            while direction != "goal":
                    robotsocket.sendall(pickle.dumps(direction))
                    print("Successfully sent a direction (" + str(direction) + ") to a robot at: " + str(address))
                    direction, robotNextPosition, new_grid_layout, goalPosition = ai.next_action_and_position_and_grid_update(self.map.width, self.map.height, self.current_layout, command[1], command[0], len(self.robots))
                    X, Y, direction = robotNextPosition
                    self.current_layout = new_grid_layout
                    self.robots[self._find_robot(address)][1] = (X, Y)
                    self.robots[self._find_robot(address)][2] = direction

        index = self._find_commands_queue(address)
        self.commands_list.pop(index)
        try:
            self.robots.remove(address)
        except:
            pass
        try:
            self.robots_manual_mode.remove(address)
        except:
            pass
        print("Disconnecting a robot at " + str(address) + "...")
        robotsocket.sendall(pickle.dumps("end"))

    def _listen_client(self, clientsocket, address):
        """
        Function for listing to a client. It continues until either the server is shutting down or the current client
        has shut down.
        Parameters
        ----------
        clientsocket: socket
            The sock for the incoming client connection.
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
                    clientsocket.sendall(pickle.dumps(self.get_robots()))
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
                            self.robots_manual_mode.append(self.robots[i])
                        except:
                            pass
                else:
                    print("Manual Mode Activated for a robot at: " + str(device))
                    try:
                        self.robots_manual_mode.append(device)
                    except:
                        pass

            elif command == "auto":
                if device == None:
                    print("Auto Mode Activated for all robots!")
                    for i in range(len(self.robots)):
                        try:
                            self.robots_manual_mode.remove(self.robots[i])
                        except:
                            pass
                else:
                    print("Auto Mode Activated for a robot at: " + str(device))
                    self.robots_manual_mode.remove(device)

            else:
                for i in range(len(self.commands_list)):
                    if self.commands_list[i].put(device):
                        self.commands_list[i].put(command)
                        print("Received " + str(command) + " to robot at " + str(device) + " from a client at: " + str(address))

        try:
            self.clients.remove(address)
        except:
            pass

        print("Disconnecting a client at " + str(address) + "...")
        clientsocket.sendall(pickle.dumps("end"))

    def _listen_camera(self, camerasocket):
        """
        Function for listing to the camera. It continues until either the server is shutting down or the camera has
        shut down.
        Parameters
        ----------
        camerasocket: socket
            The sock for the incoming camera connection.
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