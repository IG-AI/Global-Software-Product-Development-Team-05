import socket, traceback
from robot import Robot

class Server:
    def __init__(self, ip='127.0.0.1', port=2727, path='None'):
        self.ip = ip
        self.port = port

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))

        self.robot = Robot(path)

    def connect(self):
        def listen(robot, channel):
            run = True
            try:
                while run:
                    data = channel.recv(1024)
                    if not data:
                        break
                    code = data[0]
                    if (code == '\x00') | (code == '\x01') | (code == '\x02'):
                        robot.socket.send(data)
                        reply = robot.socket.recv()
                        channel.send(reply)
                    elif (code == '\x80') | (code == '\x81'):
                        robot.socket.send(data)
                    elif code == '\x98':
                        channel.send(robot.socket.type)
                    elif code == '\x99':
                        run = False
            except:
                traceback.print_exc()
            finally:
                channel.close()

        self.server.listen(1)
        while True:
            channel, details = self.server.accept()
            listen(self.robot, channel)

if __name__ == "__main__":
    Server()