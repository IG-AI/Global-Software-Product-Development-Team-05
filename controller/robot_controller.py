from flask import Flask, Blueprint, jsonify
from flask import request
import json

import authentication.login as login
from authentication.login import pre_authorized
import authentication.jwt_token_py as jwt
from model.robot import Robot
from model.account import Account
from model.adrress import Address
from util.direction import changing_direction
from util.echo_client import send
from util.write_read_map import save, load

#map = 'E E E E E\nE E E E E\nE E E E E\nE E E E E'

#HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432

robots = Blueprint('robot',__name__)

#What package belong to what robot?
def convert_map(map):
    i = 0    
    line = map.splitlines()
    while i < len(line):
        br = line[i].split(' ')
        j = 0
        while j < len(br):
            if br[j] == 'R':
                br[j] = 'O'
            elif br[j] == 'G':
                br[j] = 'E'
            #elif br = 'P':
                #br = 'O'
            j += 1
        line[i] = ' '.join(br)
        i += 1        
    map = '\n'.join(line)
    return map

def process_map(map, x, y, shell):
    #global map
    line = map.splitlines()
    br = line[-y-1].split(' ')
    br[x] = shell
    line[-y-1] = ' '.join(br)
    map = '\n'.join(line)
    print(map)
    return map

@robots.route("/api/map", methods = ['POST'])
@pre_authorized
def receive_map():
    #global map
    data = request.get_data()    
    data = json.loads(data)    
    message = data['map']    
    #message = bytes(message, 'utf-8')
    try:
        token = request.headers.get('Authorization')
        payload = jwt.decode(token[7:])
        robot_id = payload.get('sub')
        if (robot_id == None):
            raise Exception

        address = Address.find_by_id(robot_id)
        if not address:
            return jsonify({'message': 'Robot did not register host'}), 404 
        #print(map)
        map = message
        map = convert_map(map)
        print(map)
        save(map)
        message = 'map:' + message   
        message = bytes(message, 'utf-8')   
        send(address.host, PORT, message)
        #Update map
        #PAcket code goes there
    except Exception:
        return json.dumps({'message': 'Cannot connect to robot'}), 400
    return "Successful"

@robots.route("/api/auto", methods = ['POST'])
@pre_authorized
def command_auto():
    data = request.get_data()
    data = json.loads(data)
    message = data['message']
    message = bytes(message, 'utf-8')
    try:
        token = request.headers.get('Authorization')
        payload = jwt.decode(token[7:])
        robot_id = payload.get('sub')
        if (robot_id == None):
            raise Exception

        address = Address.find_by_id(robot_id)
        if not address:
            return jsonify({'message': 'Robot did not register host'}), 404 
        print(address.host)
        send(address.host, PORT, message)
        #PAcket code goes there
    except Exception:
        return json.dumps({'message': 'Cannot connect to robot'}), 400
    return "Successful"

@robots.route("/api/direction", methods = ['PUT'])
@pre_authorized
def command_direct():
    request_data = request.get_data()
    try:
        token = request.headers.get('Authorization')
        payload = jwt.decode(token[7:])
        robot_id = payload.get('sub')
        if (robot_id == None):
            raise Exception

        robot = Robot.find_by_id(robot_id)
        if not robot:
            return jsonify({'message': 'Robot not found'}), 404

        data = json.loads(request_data)
        command = data['command']

        if (command == None):
            raise Exception
        
        #Control robot go to direction relative to facing of robot
        #Server calculate new facing direction of robot relative to coordinate and save to database
        
        if (command not in ["north", "east", "south", "west", "drop"]):
            return jsonify({'message': 'Not expected command'}), 404
        current_direction = robot.current_direction
        if (command == "drop"):
            new_direction = "center"
        else: 
            new_direction = changing_direction(current_direction, command)
        message = bytes(command, 'utf-8')
       
        if (robot.role == True):
            address = Address.find_by_id(robot_id)
            if not address:
                return jsonify({'message': 'Robot did not register host'}), 404 
            send(address.host, PORT, message)
            #PAcket code goes there
    except Exception:
        return jsonify({'message': 'Invalid data'}), 404
    #Update map
    #global map
    map = load()
    map = process_map(map, robot.current_location_x, robot.current_location_y, 'E')
    robot.move(new_direction)
    robot.save_to_db()
    map = process_map(map, robot.current_location_x, robot.current_location_y, 'O')
    save(map)
    return "Successful"

@robots.route("/api/position", methods = ['GET'])
@pre_authorized
def position():
    try:
        token = request.headers.get('Authorization')
        payload = jwt.decode(token[7:])
        robot_id = payload.get('sub')
        if (robot_id == None):
            raise Exception

        robot = Robot.find_by_id(robot_id)
        if not robot:
            return jsonify({'message': 'Robot not found'}), 404
    except Exception:
        return jsonify({'message': 'Invalid data'}),404
    response = robot.serialize
    return jsonify(response), 201

@robots.route("/api/delete", methods = ['DELETE'])
@pre_authorized
def delete():
    try:
        token = request.headers.get('Authorization')
        payload = jwt.decode(token[7:])
        robot_id = payload.get('sub')
        if (robot_id == None):
            raise Exception

        robot = Robot.find_by_id(robot_id)
        if not robot:
            return jsonify({'message': 'Robot not found'}), 404
        robot.delete_from_db()        
    except Exception:
        return jsonify({'message': 'Invalid data'}),404
    return "Successful"

@robots.route("/api/create", methods = ['POST'])
@pre_authorized
def create_robot():
    request_data = request.get_data()
    print(request_data)
    try:
        token = request.headers.get('Authorization')
        payload = jwt.decode(token[7:])
        account_id = payload.get('sub')
        print(account_id)
        if (account_id == None):
            raise Exception

        account = Account.find_by_id(account_id)

        data = json.loads(request_data)
        print(data)
        current_location_x = data['x']
        current_location_y = data['y']
        current_direction = data['direction']
        current_goal_x = data['goal_x']
        current_goal_y = data['goal_y']

        robot = Robot(account_id, account.role, current_location_x, current_location_y, current_direction, current_goal_x, current_goal_y)
        robot.save_to_db()
        #Update map
    except Exception:
        return jsonify({'message': 'Invalid data'}),404
    response = robot.serialize
    return jsonify(response), 201