from queue import Queue
from time import sleep
import socket, pickle

class Client:
    """
    A class which handles a client. It can connect to a server and transmits commends for the robot(s) to the server.

    Methods
    -------
    connect(self)
        Connects the client to the server.
    send(self, commend):
        Tries to send a commend for the robot(s) to the server.
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
        commendsQueue : Queue
            A queue with commends for the robot(s).
        """
        self.SERVER_HOST = host
        self.SERVER_PORT = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)
        self.commendsQueue = Queue()

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


    def send(self, commend):
        """
        Sending a new commend for the robot(s) through the server.

        Parameters
        ----------
        commend: string
            The new commend for the robot(s).
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
            print("Trying to send new commend to server (" + str(commend) + ")...")
            self._setCommend(commend)
            self.socket.sendall(pickle.dumps(self.commendsQueue.get()))
        except:
            print("Couldn't send to server, the server is probably disconnected.")
            self.disconnect()
            return

        print("Successfully sent commend to the server! (" + str(commend) + ")")

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

    def _setCommend(self, commend):
        """
        Setting a new commend for the robot(s) in the commendsQueue.

        Parameters
        ----------
        commend: string
            The new commend for the robot(s).
        """
        self.commendsQueue.put(commend)

if __name__ == "__main__":
    client = Client()
    client.connect()
    for i in range(10):
        client.send('1')
        sleep(1)
    client.disconnect()
