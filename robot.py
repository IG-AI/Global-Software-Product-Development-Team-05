from threading import Lock

class Robot:
    def __init__(self, path='None', type='bluetooth'):
        self.socket = self.findSocket(path, type)
        self.lock = Lock()

    def findSocket(self, path, type):
        try:
            socket = Socket(path, type)
            return socket
        except IOError:
            raise Exception("Invalid path way!")


    def __del__(self):
        self.socket.close()

class Socket:
    def __init__(self, path='None', type='bluetooth'):
        self.path = path
        self.device = open(self.path, 'r+b', buffering=0)
        self.type = type

    def close(self):
        self.device.close()

    def send(self, data):
        l0 = len(data) & 0xFF
        l1 = (len(data) >> 8) & 0xFF
        d = bytes((l0, l1)) + data
        self.device.write(d)

    def recv(self):
        data = self.device.read(2)
        load0 = data[0]
        load1 = data[1]
        len = load0 + (load1 << 8)
        return self.device.read(len)
