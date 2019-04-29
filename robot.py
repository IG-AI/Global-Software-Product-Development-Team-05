import socket, pickle

class Robot:
    def __init__(self, host='127.0.1.1', port=2627):
        self.SERVER_HOST = host
        self.SERVER_PORT = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commends = []

    def __del__(self):
        self.socket.close()

    def connect(self):
        run = True
        with self.socket as socket:
            try:
                print("Connecting to server on IP: " + str(self.SERVER_HOST) + " and port: " + str(self.SERVER_PORT))
                socket.connect((self.SERVER_HOST, self.SERVER_PORT))
                socket.sendall(pickle.dumps('robot'))
            except:
                raise Exception("The robot couldn't connect to the server!")

            print("Starts executing robot...")
            while run:
                temp = pickle.loads(self.socket.recv(4096))
                if temp == "end":
                    print("Robot disconnecting...")
                    run = False
                    self.disconnect()
                    self.socket.close()
                else:
                    self.commends.append(temp)

    def disconnect(self):
        self.socket.close()

if __name__ == "__main__":
    robot = Robot()
    robot.connect()
