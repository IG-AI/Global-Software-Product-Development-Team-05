import random
import socket, pickle, _thread
from queue import Queue
from time import sleep

class Robot:
    """
    A class which handles a LEGO robot. It can connect to a server and receive commands form the server.

    Methods
    -------
    connect(self)
        Connects the robot to the server.
    recv(self, command):
        Tries to receive a command form the server.
    disconnect(self)
        Disconnects the robot to the server.
    """
    def __init__(self, host='127.0.1.1', port=2526):
        """
        Initialize the robot class, with a host and port as optional input.

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
            The robot socket.
        commandsQueue : Queue
            A queue with commands for the robot.
        """
        self.SERVER_HOST = host
        self.SERVER_PORT = port
        self.MANUAL = False
        self.RUN = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commandsQueue = Queue()

    def __del__(self):
        """
        Disconnects the robot if the robot object is removed.
        """
        self.socket.close()

    def connect(self):
        """
        Setting up the connection for the robot to the server.

        Raises
        ------
        Exception
            If the robot can't connect to the server, Exception is raised.
        """
        try:
            print("Connecting to server on IP: " + str(self.SERVER_HOST) + " and port: " + str(self.SERVER_PORT))
            self.socket.connect((self.SERVER_HOST, self.SERVER_PORT))
            self.socket.sendall(pickle.dumps('robot'))
            self.RUN = True

            self.recv(1)
        except:
            raise Exception("The robot couldn't connect to the server!")


    def recv(self, amount=None):
        """
        Tries to receive commands form the server. If input leaves emtpy it will continue until it gets a end call
        from the server. Otherwise it will receive the same amount of commands as the input.

        amount(=None): int
            The amount of commands that should be received before the function should end. Of left empty, then it will
            continue until the robot receives a end call from the server.

        Raises
        ------
        Exception
            If input isn't None or an int, Exception is raised.
        """
        if (type(amount) == int) | (amount == None):
            if amount == None:
                while True:
                    self._recvAux()
            else:
                for i in range(amount):
                    self._recvAux()
        else:
            raise Exception("Invalid input! Input has to be an int.")

    def _recvAux(self):
        """
        Aux function to the recv function.
        """
        try:
            print("Trying to receive a new command from server...")
            data = pickle.loads(self.socket.recv(4096))
            if data == "end":
                self.RUN = False
                self.disconnect()
                return
            elif data == "manual":
                print("Manual Mode activated!")
                self.MANUAL = True
            elif data == "auto":
                print("Auto Mode activated!")
                self.MANUAL = False
            elif data == "start":
                print("Robot started!")
                _thread.start_new_thread(self._startAux(), ())
            elif data == "stop":
                print("Robot stopped!")
                self.stop()
            else:
                print("Successfully received a command from the server! (" + str(data) + ")")
                self.commandsQueue.put(data)
                return
        except:
            print("Failed to receive command from server!")
            pass

    def start(self):
        """
        Function that starts the robot.
        """
        _thread.start_new_thread(self._startAux(), ())

    def _startAux(self):
        """
        Aux function to the start function.
        """
        self.RUN = True
        while self.RUN:
            self.recv(1)
            if (self.commandsQueue.empty()) & (self.MANUAL == False):
                self._createCommands()

        self.recv(1)

    def stop(self):
        """
        Function that stops the robot.
        """
        self.RUN = False

    def disconnect(self):
        """
        Closing down the connection between the robot and the server.
        """
        print("Robot disconnecting...")
        self.socket.sendall(pickle.dumps("end"))
        sleep(1)
        self.socket.close()

    def _createCommands(self):
        """
        Creates commands for the robots, if no client has sent a command.
        """
        command = str(random.randint(1, 4) * 4)
        self.commandsQueue.put(command)

if __name__ == "__main__":
    robot = Robot()
    robot.connect()