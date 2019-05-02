import socket, pickle, time

class Camera:
    def __init__(self, host='127.0.1.1', port=2627):
        self.SERVER_HOST = host
        self.SERVER_PORT = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1)
        self.videostream = None

    def __del__(self):
        self.socket.close()

    def connect(self):
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

    def disconnect(self):
        self.socket.close()

    def updateVideo(self):
        self.videostream = 1

if __name__ == "__main__":
        camera = Camera()
        camera.connect()
