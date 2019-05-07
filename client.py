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
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)
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
        except:
            raise Exception("The client couldn't connect to the server!")


    def send(self, command):
        """
        Sending a new command for the robot(s) through the server.

        Parameters
        ----------
        command: string
            The new command for the robot(s).
        """
        try:
            self.socket.settimeout(1)
            stop = pickle.loads(self.socket.recv(4096))
            if stop == "end":
                self.disconnect()
                return
        except:
            pass
        try:
            print("Trying to send new command to server (" + str(command) + ")...")
            self._setCommand(command)
            self.socket.sendall(pickle.dumps(self.commandsQueue.get()))
        except:
            print("Couldn't send to server, the server is probably disconnected.")
            self.disconnect()
            return

        print("Successfully sent command to the server! (" + str(command) + ")")

    def disconnect(self):
        """
        Closing down the connection between the client and the server.
        """
        print("Client disconnecting...")
        try:
            self.socket.sendall(pickle.dumps("end"))
        except:
            pass
        finally:
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

if __name__ == "__main__":
    client = Client()
    client.connect()
    for i in range(10):
        client.send('1')
        sleep(1)
    client.disconnect()