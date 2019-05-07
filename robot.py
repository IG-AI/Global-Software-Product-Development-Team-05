import socket, pickle
from time import sleep

class Robot:
    def __init__(self, host='127.0.1.1', port=2526):
        self.SERVER_HOST = host
        self.SERVER_PORT = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commends = []

    def __del__(self):
        self.socket.close()

    def connect(self):
        try:
            print("Connecting to server on IP: " + str(self.SERVER_HOST) + " and port: " + str(self.SERVER_PORT))
            self.socket.connect((self.SERVER_HOST, self.SERVER_PORT))
            self.socket.sendall(pickle.dumps('robot'))
            self.RUN = True
        except:
            raise Exception("The robot couldn't connect to the server!")


    def recv(self):
        try:
            print("Trying to receive new commend from server...")
            data = pickle.loads(self.socket.recv(4096))
            if data == "end":
                self.RUN = False
                self.disconnect()
                return
            else:
                print("Successfully received a commend from the server! (" + str(data) + ")")
                self.commends.append(data)
                return
        except:
            pass

    def disconnect(self):
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
