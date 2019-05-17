from flask import Flask, Blueprint, jsonify
from flask import request
import json

import authentication.login as login
from authentication.login import pre_authorized
import authentication.jwt_token_py as jwt
from model.robot import Robot
from model.account import Account
from model.adrress import Address
from util.direction import changing_direction, get_turning
from util.echo_client import send
from controller.robot_controller import process_map
from util.write_read_map import save, load

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432
absolute_move_able = {
    "north": 1,
    "east": 1,
    "south": 1,
    "west": 1
}
relative_move_able = {
    "north": 1,
    "east": 1,
    "south": 1,
    "west": 1
}


legos = Blueprint('lego',__name__)



def detect_moveable(coordinate_x, coordinate_y, request_direction_absolute):
    halt = 0
    north_moveable = 1
    east_moveable = 1
    south_moveable = 1
    west_moveable = 1
    robots = Robot.query.all()
    for robot in robots:
        if ((robot.current_location_x == coordinate_x) and (robot.current_location_y == (coordinate_y + 1))):
            north_moveable = 0
        elif ((robot.current_location_x == coordinate_x) and (robot.current_location_y == (coordinate_y - 1))):
            south_moveable = 0
        elif ((robot.current_location_x == (coordinate_x + 1)) and (robot.current_location_y == coordinate_y)):
            east_moveable = 0
        elif ((robot.current_location_x == (coordinate_x + 1)) and (robot.current_location_y == coordinate_y)):
            west_moveable = 0
        else: {}

    if ((request_direction_absolute == "north") and (north_moveable == 0)):
        halt = 1
        return halt
    elif ((request_direction_absolute == "east") and (east_moveable == 0)):
        halt = 1
        return halt
    elif ((request_direction_absolute == "south") and (south_moveable == 0)):
        halt = 1
        return halt
    elif ((request_direction_absolute == "west") and (west_moveable == 0)):
        halt = 1
        return halt
    else: 
        return halt

@legos.route("/lego", methods = ['POST'])
def log():
    #global map
    map = load()
    request_data = request.get_data()
    print(request_data)
    data = json.loads(request_data) 
    print(data)   
    try:
        absolute_direction = data['request']
        #message = bytes(message, 'utf-8')
        addr = request.remote_addr
        addr = str(addr)
        print(addr)

        address = Address.find_by_host(addr)
        print("found")
        if not address:
            return jsonify({'message': 'Unauthorized'}), 401

        robot = Robot.find_by_id(address.id)
        if not robot:
            return jsonify({'message': 'No robot found'}), 404
        #coordinate_x = robot.coordinate_x
        #coordinate_y = robot.coordinate_y
        #facing = robot.
        print("start")
        if detect_moveable(robot.current_location_x, robot.current_location_y, absolute_direction):
            send (addr, PORT, bytes('halt', 'utf-8'))
            map_send = 'map:' + map
            send(addr, PORT, bytes(map_send, 'utf-8'))
        else:
            
            #Robot read map and send move direction relative to coordinate
            #Server calculate which direction relative to robot facing need to perform so absolute move direction can be achieved
            print(map)
            map = process_map(map, robot.current_location_x, robot.current_location_y, 'E')
            relative_direction = get_turning(robot.current_direction, absolute_direction)
            message = bytes(relative_direction, 'utf-8')
            send (addr, PORT, message)
            map_send = map
            print(map_send)
            robot.move(absolute_direction)
            robot.save_to_db()
            map = process_map(map, robot.current_location_x, robot.current_location_y, 'O')
            save(map)
            map_send = process_map(map_send, robot.current_location_x, robot.current_location_y, 'R')
            map_send = process_map(map_send, robot.current_goal_x, robot.current_goal_y, 'G')
            map_send = 'map:' + map_send
            send(addr, PORT, bytes(map_send, 'utf-8'))
        #Processing map change robot's position and goal       
        #send(address.host, PORT, map)
        #Update map and robot position in database
        response = robot.serialize
    except Exception:
        return jsonify({'message': 'Error'}), 400
    return jsonify(response), 404

#May be dont need turn function
@legos.route("/lego/turn", methods = ['POST'])
def turn():
    request_data = request.get_data()
    data = json.loads(request_data)
    try:
        turn = data['turn']
        #message = bytes(message, 'utf-8')
        addr = request.remote_addr
        addr = str(addr)

        address = Address.find_by_host(addr)
        if not address:
            return jsonify({'message': 'Unauthorized'}), 401

        robot = Robot.find_by_id(address.id)
        if not robot:
            return jsonify({'message': 'No robot found'}), 404

        current_direction = robot.current_direction
        new_direction = changing_direction(current_direction, turn)
        robot.assign_direction(new_direction)
        robot.save_to_db()
        response = robot.serialize
    except Exception:
        return jsonify({'message': 'Error'}), 400
    return jsonify(response), 404

        

@legos.route("/lego/register", methods = ['POST'])
def track():
    request_data = request.get_data()
    data = json.loads(request_data)
    try:
        name = data['name']
        addr = request.remote_addr
        #print(addr)
        if ((not name) or (not addr)):
            raise Exception

        account = Account.find_by_name(name)
        if not account:
            return jsonify({'message': 'Account not found'}), 404

        #send(addr, PORT, bytes('hello', 'utf-8'))


        address = Address.find_by_id(account.id)
        if not address:
            address = Address(account.id, addr)
        else:
            address.assign_address(addr)
        address.save_to_db()
    except Exception:
        return jsonify({'message': 'Invalid data'}), 404
    return jsonify({'message': 'Successful'}), 404