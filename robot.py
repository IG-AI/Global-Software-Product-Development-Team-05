import socket, pickle
from queue import Queue
from time import sleep

class Robot:
    """
    A class which handles a LEGO robot. It can connect to a server and receive commends form the server.

    Methods
    -------
    connect(self)
        Connects the robot to the server.
    recv(self, commend):
        Tries to receive a commend form the server.
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
        commendsQueue : Queue
            A queue with commends for the robot.
        """
        self.SERVER_HOST = host
        self.SERVER_PORT = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commendsQueue = Queue()

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
        except:
            raise Exception("The robot couldn't connect to the server!")


    def recv(self):
        """
        Tries to receive a commend form the server.
        """
        try:
            print("Trying to receive new commend from server...")
            data = pickle.loads(self.socket.recv(4096))
            if data == "end":
                self.RUN = False
                self.disconnect()
                return
            else:
                print("Successfully received a commend from the server! (" + str(data) + ")")
                self.commendsQueue.put(data)
                return
        except:
            pass

    def disconnect(self):
        """
        Closing down the connection between the robot and the server.
        """
        print("Robot disconnecting...")
        try:
            self.socket.sendall(pickle.dumps("end"))
        except:
            pass
        finally:
            self.socket.close()

if __name__ == "__main__":
    robot = Robot()
    robot.connect()
    for i in range(10):
        robot.recv()
        sleep(1)
    robot.disconnect()
