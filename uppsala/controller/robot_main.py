#!/usr/bin/env python3
"""
Control code for the physical robot, this file together with peer and robot should be loaded on to the LEGO brick with ev3dev installed.

Author: Daniel Ågstrand
"""

from ev3dev2.motor import LargeMotor, MoveSteering, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sound import Sound

import robot

robot = robot.Robot()
robot.connect()