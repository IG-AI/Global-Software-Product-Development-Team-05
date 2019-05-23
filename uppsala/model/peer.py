import socket

class Peer:
    """
    Base class for the server, robot and client

    Author: Daniel Ågstrand
    """
    def __init__(self, server_ip="127.0.0.1", server_port=2525):
        """
        Initialize the peer class, with a server ip and port as optional input.

        Parameters
        ----------
        server_ip(='127.0.1.1'): string
            A string with the IP address for which the server should use.
        server_port(=2526): int
            A port number the server server should use.

        Attributes
        ----------
        server_ip : string
            The servers host address.
        server_port : int
            The servers port number.
        sock : socket
            The peer sock.
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)