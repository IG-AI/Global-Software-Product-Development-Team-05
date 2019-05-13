import socket, pickle

class Camera:
    """
    A class which handles a camera. It can connect to a server and transmit a video stream.

    Methods
    -------
    connect(self)
        Connects the camera to the server.
    disconnect(self)
        Disconnects the camera to the server.
    updateVideo(self)
        Updates the video stream from the camera.
    """
    def __init__(self, host='127.0.1.1', port=2526):
        """
        Initialize the camera class, with a host and port as optional input.

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
            The camera socket.
        videostream : Video Stream
            The video stream captured from the camera.
        """
        self.SERVER_HOST = host
        self.SERVER_PORT = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1)
        self.videostream = None

    def __del__(self):
        """
        Disconnects the camera if the camera object is removed.
        """
        self.socket.close()

    def connect(self):
        """
        Setting up the connection for the camera to the server.

        Raises
        ------
        Exception
            If the camera can't connect to the server, Exception is raised.
        """
        run = True
        with self.socket as socket:
            try:
                print(
                    "Connecting to server on IP: " + str(self.SERVER_HOST) + " and port: " + str(self.SERVER_PORT))
                socket.connect((self.SERVER_HOST, self.SERVER_PORT))
                socket.sendall(pickle.dumps('camera'))
            except:
                raise Exception("The camera couldn't connect to the server!")

            print("Starts executing camera...")
            while run:
                try:
                    data = pickle.loads(self.socket.recv(4096))
                    if data == "end":
                        print("Camera disconnecting...")
                        run = False
                        self.disconnect()
                        self.socket.close()
                except:
                    pass
                try:
                    self.updateVideo()
                    socket.sendall(pickle.dumps(self.videostream))
                except:
                    pass

    def updateVideo(self):
        """
        Updates the video stream from the camera.
        """
        self.videostream = 1

    def disconnect(self):
        """
        Closing down the connection between the camera and the server.
        """
        self.socket.close()

if __name__ == "__main__":
        camera = Camera()
        camera.connect()