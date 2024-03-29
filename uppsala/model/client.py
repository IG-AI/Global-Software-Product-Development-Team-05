from queue import Queue
from time import sleep
import socket, pickle
from model.peer import Peer

class Client(Peer):
    """
    A class which handles a client. It can connect to a server and transmits commands for the robot(s) to the server.

    Methods
    -------
    connect(self):
        Connects the client to the server.
    send_command(self, pickup, command, robot=None):
        Tries to send a command for either a specific robot or to all robots if robot=None through the server.
    activate_manual_mode(self, robot=None):
        Activates manual mode for either a specific robot or to all robots if robot=None through the server.
    deactivate_manual_mode(self, robot=None):
        Dectivates manual mode for either a specific robot or to all robots if robot=None through the server.
    disconnect(self):
        Disconnects the client to the server.

    Author: Daniel Ågstrand
    """
    def __init__(self, server_ip='127.0.0.1', server_port=2526):
        """
        Initialize the client class, with a host and server_port as optional input.

        Parameters
        ----------
        host(='127.0.1.1'): string
            A string with the IP address to the server.
        server_port(=2526): int
            A server_port number to the server.

        Attributes
        ----------
        server_ip: string
            The servers host address.
        server_port: int
            The servers server_port number.
        commands_queue: Queue
            A queue with coordinates that a robot(s) should move_to_coords towards.
        """
        super(Client, self).__init__(server_ip, server_port)
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_robots_list = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)
        self.map = None
        self.commands_queue = Queue()

    def __del__(self):
        """
        Disconnects the client if the client object is removed.
        """
        self.sock.close()

    def connect(self):
        """
        Setting up the connection for the client to the server.

        Raises
        ------
        Exception
            If the client can't connect to the server, Exception is raised.
        """
        try:
            print("Connecting to server on IP: " + str(self.server_ip) + " and port: " + str(self.server_port))
            self.sock.connect((self.server_ip, self.server_port))
            self.sock.sendall(pickle.dumps('client'))
            self._update_robots_list()
            self._update_map()
        except:
            raise Exception("The client couldn't connect to the server!")


    def send_command(self, pickup, command, robot=None):
        """
        Sending a new command for the robot(s) through the server.

        Parameters
        ----------
        pickup: boolean
            Flag the indicates if the robot should pickup or drop off the package.
        command: string
            The new command for the robot(s).
        robot(=None): string
            Address in the the form (IP, PORT) for the robot how should receive the command. If None, then the command
            will be sent to all connected robots.
        """
        self._update_robots_list()
        if len(self.server_robots_list) > 0:
            if (robot != None) | (robot in self.server_robots_list):
                try:
                    self.sock.settimeout(1)
                    stop = pickle.loads(self.sock.recv(4096))
                    if stop == "end":
                        self.disconnect()
                        return
                except:
                    pass

                if robot==None:
                    print("Trying to send a new command (" + str(command) + ") to all robots")
                else:
                    print("Trying to send a new command (" + str(command) + ") to a robot at: " + str(robot))
                for i in range(len(self.server_robots_list)):
                    try:
                        self._set_command(pickup, command)
                        self.sock.sendall(pickle.dumps((robot, self.commands_queue.get())))
                    except:
                        print("Couldn't send to server, the server is probably disconnected.")
                        self.disconnect()
                        return

                print("Successfully sent command to the server! (" + str(command) + ")")
            else:
                print("Robot isn't connected to the server!")
        else:
            print("There isn't any robots connected to the server!")

    def activate_manual_mode(self, robot=None):
        """
        Activates manual mode for a robot(s), so it starts to only listing for commands from clients.

        Parameters
        ----------
        robot(=None): string
            Address in the the form (IP, PORT) for the robot how should receive the manual mode command. If None, then
            the command will be sent to all connected robots.
        """
        try:
            self.sock.settimeout(1)
            stop = pickle.loads(self.sock.recv(4096))
            if stop == "end":
                self.disconnect()
                return
        except:
            pass

        if robot == None:
            print("Activating manual mode for all robots!")
            self._update_robots_list()
            for i in range(len(self.server_robots_list)):
                self.sock.sendall(pickle.dumps((self.server_robots_list[i], "manual")))
        else:
            print("Activating manual mode for a robot at : " + str(robot))
            self._update_robots_list()
            self.sock.sendall(pickle.dumps((robot, "manual")))

    def deactivate_manual_mode(self, robot=None):
        """
        Deactivates manual mode for a robot(s), so it starts moving automatically.

        Parameters
        ----------
        robot(=None): string
            Address in the the form (IP, PORT) for the robot how should receive the auto mode command. If None, then
            the command will be sent to all connected robots.
        """
        try:
            self.sock.settimeout(1)
            stop = pickle.loads(self.sock.recv(4096))
            if stop == "end":
                self.disconnect()
                return
        except:
            pass

        if robot == None:
            print("Deactivating manual mode for all robots!")
            self._update_robots_list()
            for i in range(len(self.server_robots_list)):
                self.sock.sendall(pickle.dumps((self.server_robots_list[i], "auto")))
        else:
            print("Deactivating manual mode for a robot at : " + str(robot))
            self.sock.sendall(pickle.dumps((robot, "auto")))

    def disconnect(self):
        """
        Closing down the connection between the client and the server.
        """
        print("Client disconnecting...")
        sleep(1)
        self.sock.sendall(pickle.dumps((self.sock.getsockname(), "end")))
        self.sock.close()

    def _set_command(self, pickup, command):
        """
        Setting a new command for the robot(s) in the direction_queue.

        Parameters
        ----------
        command: string
            The new command for the robot(s).
        """
        self.commands_queue.put([pickup, command])

    def _update_robots_list(self):
        """
        Updates the robots list with help of of the _recv_robots function.
        """
        self.server_robots_list = self._recv_robots()


    def _recv_robots(self):
        """
        Receive the robots list from the server.

        Returns
        -------
        [] if server is shutting down or if it couldn't receive the robot list. Otherwise returns the robot_list.
        """
        try:
            self.sock.settimeout(1)
            stop = pickle.loads(self.sock.recv(4096))
            if stop == "end":
                self.disconnect()
                return []
        except:
            pass

        self.sock.sendall(pickle.dumps((None, "robotlist")))

        try:
            print("Trying to receive robot list from server...")
            sleep(1)
            robotlist = pickle.loads(self.sock.recv(4096))
            print("Successfully received robot list from server!")
            return robotlist
        except:
             print("Failed to receive robot list from server...")
             return []

    def _update_map(self):
        """
        Updates the layout map over the area the robot operates in.
        """
        self.map = self._recv_map()

    def _recv_map(self):
        """
        Receive the map from the server.

        Returns
        -------
        [] if server is shutting down, None if it couldn't receive any maps and otherwise returns the map in the form of
        a matrix.
        """
        try:
            self.sock.settimeout(1)
            stop = pickle.loads(self.sock.recv(4096))
            if stop == "end":
                self.disconnect()
                return []
        except:
            pass

        self.sock.sendall(pickle.dumps((None, "map")))

        try:
            print("Trying to receive map from server...")
            sleep(1)
            map = pickle.loads(self.sock.recv(4096))
            print("Successfully received map from server!")
            return map
        except:
            print("Failed to receive map from server, probably the server that doesn't have access to any map ...")
            return None