from queue import Queue
from time import sleep
import socket, pickle

class Client:
    """
    A class which handles a client. It can connect to a server and transmits commands for the robot(s) to the server.

    Methods
    -------
    connect(self)
        Connects the client to the server.
    send(self, command):
        Tries to send a command for the robot(s) to the server.
    disconnect(self)
        Disconnects the client to the server.
    """
    def __init__(self, host='127.0.1.1', port=2526):
        """
        Initialize the client class, with a host and port as optional input.

        Parameters
        ----------
        host(='127.0.1.1'): string
            A string with the IP address to the server.
        port(=2526): int
            A port number to the server.

        Attributes
        ----------
        SERVER_HOST: string
            The servers host address.
        SERVER_PORT : int
            The servers port number.
        socket : socket
            The client socket.
        commandsQueue : Queue
            A queue with commands for the robot(s).
        """
        self.SERVER_HOST = host
        self.SERVER_PORT = port
        self.SERVER_ROBOTSLIST = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(10)
        self.commandsQueue = Queue()

    def __del__(self):
        """
        Disconnects the client if the client object is removed.
        """
        self.socket.close()

    def connect(self):
        """
        Setting up the connection for the client to the server.

        Raises
        ------
        Exception
            If the client can't connect to the server, Exception is raised.
        """
        try:
            print("Connecting to server on IP: " + str(self.SERVER_HOST) + " and port: " + str(self.SERVER_PORT))
            self.socket.connect((self.SERVER_HOST, self.SERVER_PORT))
            self.socket.sendall(pickle.dumps('client'))
            self._updateRobotsList()
        except:
            raise Exception("The client couldn't connect to the server!")


    def sendCommand(self, command, robot=None):
        """
        Sending a new command for the robot(s) through the server.

        Parameters
        ----------
        command: string
            The new command for the robot(s).
        robot(=None): string
            Address in the the form (IP, PORT) for the robot how should receive the command. If None, then the command
            will be sent to all connected robots.
        """
        self._updateRobotsList()
        if len(self.SERVER_ROBOTSLIST) > 0:
            if (robot != None) & (robot in self.SERVER_ROBOTSLIST):
                try:
                    self.socket.settimeout(1)
                    stop = pickle.loads(self.socket.recv(4096))
                    if stop == "end":
                        self.disconnect()
                        return
                except:
                    pass

                if robot==None:
                    print("Trying to send a new command (" + str(command) + ") to all robots")
                else:
                    print("Trying to send a new command (" + str(command) + ") to a robot at: " + str(robot))
                try:
                    self._setCommand(command)
                    self.socket.sendall(pickle.dumps((robot, self.commandsQueue.get())))
                except:
                    print("Couldn't send to server, the server is probably disconnected.")
                    self.disconnect()
                    return

                print("Successfully sent command to the server! (" + str(command) + ")")
            else:
                print("Robot isn't connected to the server!")
        else:
            print("There isn't any robots connected to the server!")

    def activateManualMode(self, robot=None):
        """
        Activates manual mode for a robot(s), so it starts to only listing for commands from clients.

        Parameters
        ----------
        robot(=None): string
            Address in the the form (IP, PORT) for the robot how should receive the manual mode command. If None, then
            the command will be sent to all connected robots.
        """
        try:
            self.socket.settimeout(1)
            stop = pickle.loads(self.socket.recv(4096))
            if stop == "end":
                self.disconnect()
                return
        except:
            pass

        if robot == None:
            print("Activating manual mode for all robots!")
        else:
            print("Activating manual mode for a robot at : " + str(robot))
        self._updateRobotsList()
        self.socket.sendall(pickle.dumps((robot, "manual")))

    def deactivateManualMode(self, robot=None):
        """
        Deactivates manual mode for a robot(s), so it starts moving automatically.

        Parameters
        ----------
        robot(=None): string
            Address in the the form (IP, PORT) for the robot how should receive the auto mode command. If None, then
            the command will be sent to all connected robots.
        """
        try:
            self.socket.settimeout(1)
            stop = pickle.loads(self.socket.recv(4096))
            if stop == "end":
                self.disconnect()
                return
        except:
            pass

        if robot == None:
            print("Deactivating manual mode for all robots!")
        else:
            print("Deactivating manual mode for a robot at : " + str(robot))
        self._updateRobotsList()
        self.socket.sendall(pickle.dumps((robot, "auto")))

    def disconnect(self):
        """
        Closing down the connection between the client and the server.
        """
        print("Client disconnecting...")

        self.socket.sendall(pickle.dumps((None, "end")))
        sleep(1)
        self.socket.close()

    def _setCommand(self, command):
        """
        Setting a new command for the robot(s) in the commandsQueue.

        Parameters
        ----------
        command: string
            The new command for the robot(s).
        """
        self.commandsQueue.put(command)

    def _updateRobotsList(self):
        """
        Updates the robots list with help of of the _recvRobots function.
        """
        self.SERVER_ROBOTSLIST = self._recvRobots()


    def _recvRobots(self):
        """
        Receive the robots list from the server.
        """
        try:
            self.socket.settimeout(1)
            stop = pickle.loads(self.socket.recv(4096))
            if stop == "end":
                self.disconnect()
                return []
        except:
            pass

        self.socket.sendall(pickle.dumps((None, "robotlist")))
        try:
            print("Trying to receive robot list from server...")
            robotlist = pickle.loads(self.socket.recv(4096))
            print("Successfully received robot list from server!")
            return robotlist
        except:
            print("Failed to receive robot list from server...")
            return []

if __name__ == "__main__":
    client = Client()
    client.connect()
    client.activateManualMode()
    for i in range(5):
        if len(client.SERVER_ROBOTSLIST) > 0:
            client.sendCommand('1', client.SERVER_ROBOTSLIST[0])
    client.deactivateManualMode()
    client.disconnect()