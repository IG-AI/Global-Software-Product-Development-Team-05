import random
import socket, pickle, _thread
from queue import Queue
from time import sleep
from db import DB
from model.base import Base
import nxt

PORT_A = 0x00
PORT_B = 0x01
PORT_C = 0x02
PORT_D = 0x03

class Robot(Base):
    """
    A class which handles a LEGO robot. It can connect to a server and receive commands form the server.

    Methods
    -------
    connect(self)
        Connects the robot to the server.
    recv(self, command):
        Tries to receive a command form the server.
    disconnect(self)
        Disconnects the robot to the server.
    """
    __tablename__ = 'robot'

    id = DB.Column(DB.Integer, primary_key=True)
    role = DB.Column(DB.Boolean)
    current_location_x = DB.Column(DB.Integer)
    current_location_y = DB.Column(DB.Integer)
    current_direction = DB.Column(DB.String(20))

    def __init__(self, id, role, current_location_x, current_location_y, current_direction, host='127.0.1.1', port=2526, pos=(1, 1)):
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
        commandsQueue : Queue
            A queue with commands for the robot.
        """
        self.SERVER_HOST = host
        self.SERVER_PORT = port
        self.MANUAL = False
        self.RUN = False
        self.BRICK = nxt.locator.find_one_brick(name = 'MyRobot')
        self.brickName, self.brickHost, self.brickSignalStrength, self.brickUserFlash = self.BRICK.get_device_info()
        self.LEFT_MOTOR = nxt.Motor(self.BRICK, PORT_A)
        self.RIGHT_MOTOR = nxt.Motor(self.BRICK, PORT_B)
        self.LIGHT_SENSOR = nxt.Color20(self.BRICK, PORT_C)
        self.LIGHT_SENSOR.set_light_color(nxt.Type.COLORRED)
        self.TEMPERATURE_SENSOR = nxt.Temperature(self.BRICK, PORT_D)
        self.POS = pos
        self.id = id
        self.role = role
        self.current_location_x = current_location_x
        self.current_location_y = current_location_y
        self.current_direction = current_direction
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commandsQueue = Queue()

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

            self.recv(1)
        except:
            raise Exception("The robot couldn't connect to the server!")


    def recv(self, amount=None):
        """
        Tries to receive commands form the server. If input leaves emtpy it will continue until it gets a end call
        from the server. Otherwise it will receive the same amount of commands as the input.

        Parameters
        ----------
        amount(=None): int
            The amount of commands that should be received before the function should end. Of left empty, then it will
            continue until the robot receives a end call from the server.

        Raises
        ------
        Exception:
            If input isn't None or an int, Exception is raised.
        """
        if (type(amount) == int) | (amount == None):
            if amount == None:
                while True:
                    self._recvAux()
            else:
                for i in range(amount):
                    self._recvAux()
        else:
            raise Exception("Invalid input! Input has to be an int.")

    def _recvAux(self):
        """
        Aux function to the recv function.
        """
        try:
            print("Trying to receive a new command from server...")
            data = pickle.loads(self.socket.recv(4096))
            if data == "end":
                self.RUN = False
                self.disconnect()
                return
            elif data == "manual":
                print("Manual Mode activated!")
                self.MANUAL = True
            elif data == "auto":
                print("Auto Mode activated!")
                self.MANUAL = False
            elif data == "start":
                print("Robot started!")
                _thread.start_new_thread(self._startAux(), ())
            elif data == "stop":
                print("Robot stopped!")
                self.stop()
            else:
                print("Successfully received a command from the server! (" + str(data) + ")")
                self.commandsQueue.put(data)
                return
        except:
            print("Failed to receive command from server!")
            pass

    def start(self):
        """
        Function that starts the robot.
        """
        _thread.start_new_thread(self._startAux(), ())

    def _startAux(self):
        """
        Aux function to the start function.
        """
        self.BRICK.play_tone_and_wait(500, 5)
        self.RUN = True
        while self.RUN:
            self.recv(1)
            if (self.commandsQueue.empty()) & (self.MANUAL == False):
                self._createCommands()

        self.recv(1)

    def stop(self):
        """
        Function that stops the robot.
        """
        self.BRICK.play_tone_and_wait(300, 5)
        self.RUN = False

    def turn(self, direction):
        """
        Turns the robot 90 degrees, either to left or right based on the input.

        Parameters
        ----------
        direction ("left"/"right): string
            The direction the robot should turn.

        Raises
        ------
            Exception:
                If the input isn't "left" or "right", Exception is raised.
        """
        if direction == 'left':
            self.LEFT_MOTOR.turn(64, 90)
            self.RIGHT_MOTOR.turn(-64, 90)
        elif direction == 'right':
            self.LEFT_MOTOR.turn(-64, 90)
            self.RIGHT_MOTOR.turn(64, 90)
        else:
            raise Exception("The wheels can only turn either left or right!")

    def run(self, speed=64):
        """
        Starts the motors, with the speed as the input, as the default 64

        Parameters
        ----------
        speed (=64): int
            The speed the robot should run in.

        Raises
        ------
            Exception:
                If the input isn't an int, Exception is raised.
        """
        if type(speed) is int:
            self.LEFT_MOTOR.run(speed)
            self.RIGHT_MOTOR.run(speed)
        else:
            raise Exception("The speed has to be an int!")

    def brake(self):
        """
        Breaks the robots movement.
        """
        self.LEFT_MOTOR.brake()
        self.RIGHT_MOTOR.brake()

    def disconnect(self):
        """
        Closing down the connection between the robot and the server.
        """
        print("Robot disconnecting...")
        self.socket.sendall(pickle.dumps("end"))
        sleep(1)
        self.BRICK.sock.close()
        self.socket.close()

    """
    def updatePos(self):
        if not self.commandsQueue.empty():
            newPos = self.commandsQueue.get()
            X, Y = self.POS
            newX, newY = newPos

            if newX > X:
                self.turn('right')

            elif newX < X:
                self.turn('r')

            if self.POS == newPos:
                print("Robot reached it destination at: " + self.POS)
                self.brake()
            else:
                    while True:
                        if self.LIGHT_SENSOR.get_color() > 75:
                            X =+ 1

                elif newX < X:
    """

    @property
    def serialize(self):
        return {
            'id': self.id,
            'current_location_x': self.current_location_x,
            'current_location_y': self.current_location_y,
            'current_direction': self.current_direction
        }

    def assign_coordinate(self, current_location_x, current_location_y, current_direction):
        self.current_location_x = current_location_x
        self.current_location_y = current_location_y
        self.current_direction = current_direction

    def move(self, direction):
        if (direction == "north"):
            self.current_location_y += 1
        elif (direction == "east"):
            self.current_location_x += 1
        elif (direction == "south"):
            self.current_location_y -= 1
        elif (direction == "west"):
            self.current_location_x -= 1
        elif (direction == "center"):
            {}
        else:
            return 1

    @classmethod
    def find_by_id(cls, id):
        packet = cls.query.filter_by(id = id).first()
        return packet