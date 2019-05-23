# !/usr/bin/env python3

import socket, pickle, _thread, serial
from queue import Queue
from time import sleep
from model.peer import Peer


class Robot(Peer):
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
    turn_cardinal(self, direction):
        Turns the robot 90 degrees, either to left or right based on the input which should be left or right.
    run(self, speed=64):
        Starts the motors, with the speed as the input, as the default 64.
    start(self):
        Function that starts the robot in a new thread.
    brake(self):
        Stops the robots motors.
    disconnect(self)
        Disconnects the robot to the server.

    Author: Daniel Ågstrand
    """

    def __init__(self, current_location_x=0, current_location_y=0, current_direction="north", server_ip='127.0.1.1', server_port=2526):
        """
        Initialize the robot class, with a server_ip and server_port as optional input.
        Parameters
        ----------
        server_ip(='127.0.1.1'): string
            A string with the IP address to the server.
        server_port(=2526): int
            A server_port number to the server.
        Attributes
        ----------
        server_host: string
            The servers server_ip address.
        server_port : int
            The servers server_port number.
        MANUAL: boolean
            Flag that's indicates if the robot is in manual mode.
        RUN: bollean
            Flag that's indicates if the robot is running.
        direction_queue : Queue
            A queue with coordinate the robot should move_to_coords towards.
        """
        super(Robot, self).__init__(server_ip, server_port)
        self.MANUAL = False
        self.RUN = False
        self.PICKUP = True
        self.current_location_x = current_location_x
        self.current_location_y = current_location_y
        self.assign_coordinate(current_location_x, current_location_y, current_direction)
        self.direction_queue = Queue()

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
            print("Connecting to server on IP: " + str(self.server_ip) + " and port: " + str(self.server_port))
            self.sock.connect((self.server_ip, self.server_port))
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
                print("Successfully received a direction from the server! (" + str(data) + ")")
                self.direction_queue.put(data)
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
        self.RUN = True
        while self.RUN:
            self.recv(1)
            self.move()

            self.sock.sendall(pickle.dumps("done"))

        self.recv(1)

    def stop(self):
        """
        Function that stops the robot.
        """
        self.speaker.speak("Bye Bye Bitchers!")
        self.RUN = False

    def disconnect(self):
        """
        Closing down the connection between the robot and the server.
        """
        print("Robot disconnecting...")
        self.sock.sendall(pickle.dumps("end"))
        sleep(1)
        self.sock.close()

    def move(self):
        """
        Moves the robot sequentially, one cell at the time until i

        Raises
        ------
        Exception:
            If the command isn't in the format (x, y), Exception is raised.

        Returns
        -------
        not_move if no directions are available, otherwise it doesn't return anything.
        """
        try:
            direction = self.direction_queue.get()
        except:
            print("No directions available!")
            return "not_move"

        if direction == "pickup":
            print("Robot reached it destination!")

        elif direction == "dropoff":
            print("Robot reached it destination!")

        elif direction == "forward":
            pass

        elif direction == "backward":
            pass

        elif direction == "right":
            if self.current_direction == "north":
                self.current_direction = "east"
            elif self.current_direction == "south":
                self.current_direction = "west"
            elif self.current_direction == "west":
                self.current_direction = "north"
            elif self.current_direction == "east":
                self.current_direction = "south"

        elif direction == "left":
            if self.current_direction == "north":
                self.current_direction = "west"
            elif self.current_direction == "south":
                self.current_direction = "east"
            elif self.current_direction == "west":
                self.current_direction = "south"
            elif self.current_direction == "east":
                self.current_direction = "north"

        elif direction == False:
            print("No no path to the goal could be calculated!")

        else:
            raise Exception("The direction in move() has to be either, goal, forward, backward, right or left!")

        self.sock.sendall(pickle.dumps(["pos", (self.current_location_x, self.current_location_y)]))

    def assign_coordinate(self, current_location_x, current_location_y, current_direction):
        """
        Assign a coordinate to the robot.

        Parameters
        ----------
        current_location_x: int
            The current x position
        current_location_y: int
            The current y position
        current_direction: string
            The current cardinal direction the robot is facing, should be either "north", "south", "west", "east"
            and "center"
        """
        self.current_location_x = current_location_x
        self.current_location_y = current_location_y
        self.current_direction = current_direction

    def _update_current_position(self, direction, forward=True):
        """
        Updates the coordinate for the robot.

        Parameters
        ----------
        direction: string
            A cardinal direction, should be either "north", "south", "west", "east" and "center"

        Returns
        ------
        1
        """
        if forward:
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
        else:
            if (direction == "north"):
                self.current_location_y -= 1
            elif (direction == "east"):
                self.current_location_x -= 1
            elif (direction == "south"):
                self.current_location_y += 1
            elif (direction == "west"):
                self.current_location_x += 1
            elif (direction == "center"):
                {}
            else:
                return 1