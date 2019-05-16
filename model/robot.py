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
    connect(self):
        Connects the robot to the server.
    recv(self, command):
        Tries to receive a command form the server.
    start(self):
        Function that starts the robot in a new thread.
    stop(self):
        Function that stops the robot.
    turn(self, direction):
        Turns the robot 90 degrees, either to left or right based on the input which should be left or right.
    run(self, speed=64):
        Starts the motors, with the speed as the input, as the default 64.
    start(self):
        Function that starts the robot in a new thread.
    brake(self):
        Stops the robots motors.
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
        MANUAL: boolean
            Flag that's indicates if the robot is in manual mode.
        RUN: bollean
            Flag that's indicates if the robot is running.
        brick: brick
            The LEGO brick object.
        left_motor: Motor
            Motor object that controls the left motor of the robot.
        right_motor: Motor
            Motor object that controls the right motor of the robot.
        light_sensor: Color20
            Light sensor object for the robot.
        temperature_sensor: Temperature
            Temperature sensor object for the robot.
        sock : socket
            The robot sock.
        commands_queue : Queue
            A queue with commands for the robot.
        """
        self.SERVER_HOST = host
        self.SERVER_PORT = port
        self.MANUAL = False
        self.RUN = False
        self.brick = nxt.locator.find_one_brick(name ='MyRobot')
        self.brick_name, self.brick_host, self.brick_signal_strength, self.brick_user_flash = self.brick.get_device_info()
        self.left_motor = nxt.Motor(self.brick, PORT_A)
        self.right_motor = nxt.Motor(self.brick, PORT_B)
        self.light_sensor = nxt.Color20(self.brick, PORT_C)
        self.light_sensor.set_light_color(nxt.Type.COLORRED)
        self.temperature_sensor = nxt.Temperature(self.brick, PORT_D)
        self.id = id
        self.role = role
        self.current_location_x = current_location_x
        self.current_location_y = current_location_y
        self.current_direction = current_direction
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commands_queue = Queue()

    def __del__(self):
        """
        Disconnects the robot if the robot object is removed.
        """
        self.sock.close()

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
            self.sock.connect((self.SERVER_HOST, self.SERVER_PORT))
            self.sock.sendall(pickle.dumps('robot'))
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
                    self._recv_aux()
            else:
                for i in range(amount):
                    self._recv_aux()
        else:
            raise Exception("Invalid input! Input has to be an int.")

    def _recv_aux(self):
        """
        Aux function to the recv function.
        """
        try:
            print("Trying to receive a new command from server...")
            data = pickle.loads(self.sock.recv(4096))
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
                _thread.start_new_thread(self._start_aux(), ())
            elif data == "stop":
                print("Robot stopped!")
                self.stop()
            else:
                print("Successfully received a command from the server! (" + str(data) + ")")
                self.commands_queue.put(data)
                return
        except:
            print("Failed to receive command from server!")
            pass

    def start(self):
        """
        Function that starts the robot in a new thread.
        """
        _thread.start_new_thread(self._start_aux(), ())

    def _start_aux(self):
        """
        Aux function to the start function.
        """
        self.brick.play_tone_and_wait(500, 5)
        self.RUN = True
        while self.RUN:
            self.recv(1)
            if (self.commands_queue.empty()) & (self.MANUAL == False):
                self._createCommands()

        self.recv(1)

    def stop(self):
        """
        Function that stops the robot.
        """
        self.brick.play_tone_and_wait(300, 5)
        self.RUN = False

    def turn(self, direction):
        """
        Turns the robot 90 degrees, either to left or right based on the input.

        Parameters
        ----------
        direction: string
            The cardinal direction the robot should face.

        Raises
        ------
            Exception:
                If the input isn't either east, west, north or south, Exception is raised.
        """
        if (direction == "west") | (direction == "east") | (direction == "north") | (direction == "south"):
            if self.current_direction != direction:
                if self.current_direction == "west":
                    if direction == "east":
                        self.left_motor.turn(64, 180)
                        self.right_motor.turn(-64, 180)
                    elif direction == "north":
                        self.left_motor.turn(64, 90)
                        self.right_motor.turn(-64, 90)
                    elif direction == "south":
                        self.left_motor.turn(-64, 90)
                        self.right_motor.turn(64, 90)

                elif self.current_direction == "east":
                    if direction == "west":
                        self.left_motor.turn(64, 180)
                        self.right_motor.turn(-64, 180)
                    elif direction == "north":
                        self.left_motor.turn(64, 90)
                        self.right_motor.turn(-64, 90)
                    elif direction == "south":
                        self.left_motor.turn(-64, 90)
                        self.right_motor.turn(64, 90)

                elif self.current_direction == "north":
                    if direction == "west":
                        self.left_motor.turn(64, 90)
                        self.right_motor.turn(-64, 90)
                    elif direction == "east":
                        self.left_motor.turn(-64, 90)
                        self.right_motor.turn(64, 90)
                    elif direction == "south":
                        self.left_motor.turn(64, 90)
                        self.right_motor.turn(-64, 180)

                elif self.current_direction == "south":
                        if direction == "west":
                            self.left_motor.turn(-64, 90)
                            self.right_motor.turn(64, 90)
                        elif direction == "east":
                            self.left_motor.turn(64, 90)
                            self.right_motor.turn(-64, 90)
                        elif direction == "north":
                            self.left_motor.turn(-64, 180)
                            self.right_motor.turn(64, 180)

                self.current_direction = direction
            else:
                pass
        else:
            raise Exception("The direction has to be a string with either west, east, north and south!")

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
            if self.left_motor.idle():
                self.left_motor.run(speed)
                self.right_motor.run(speed)
            else:
                pass
        else:
            raise Exception("The speed has to be an int!")

    def brake(self):
        """
        Breaks the robots movement.
        """
        self.left_motor.brake()
        self.right_motor.brake()

    def disconnect(self):
        """
        Closing down the connection between the robot and the server.
        """
        print("Robot disconnecting...")
        self.sock.sendall(pickle.dumps("end"))
        sleep(1)
        self.brick.sock.close()
        self.sock.close()


    def move(self):
        """
        Moves the robot to the first coordinate in the commands_queue, if it's empty and manual mode isn't activated
        then it automatic creates a new command.

        Raises
        ------
        If the command isn't in the format (x, y), Exception is raised.
        """
        if (self.commands_queue.empty()) & (self.MANUAL == False):
            self._create_auto_commands()

        try:
            X, Y = self.commands_queue.get()
        except :
            raise Exception("Wrong format of the coordinates from the server!")

        if self.current_location_x < X:
            self.turn("east")
        else:
            self.turn("west")

        self.run()
        while (self.current_location_x != X):
            if self.light_sensor.get_color() > 75:
                self._update_current_direction(self.current_direction)
            else:
                pass

        if self.current_location_y < Y:
            self.turn("south")
        else:
            self.turn("north")

        self.brake()

        self.run()
        while (self.current_location_y != Y):
            if self.light_sensor.get_color() > 75:
                self._update_current_direction(self.current_direction)
            else:
                pass

        self.brake()

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

    def _create_auto_commands(self): # -- TODO: Add the automatic function.
        self.commands_queue.put(5,5)

    def _update_current_direction(self, direction):
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