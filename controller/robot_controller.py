from flask import Flask, Blueprint, jsonify
from flask import request
import json
#from sqlalchemy.orm import sessionmaker

import authentication.login as login
from authentication.login import pre_authorized
import authentication.jwt_token_py as jwt
from model.robot import Robot
from model.account import Account
from util.direction import changing_direction

robots = Blueprint('robot',__name__)

@robots.route("/api/map", methods = ['POST'])
@pre_authorized
def map():
    try:
        {}
        #PAcket code goes there
    except Exception:
        return json.dumps({'message': 'Cannot connect to robot'}), 400
    return "Successful"

@robots.route("/api/auto", methods = ['POST'])
@pre_authorized
def command_auto():
    try:
        {}
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

        if (command not in ["north", "east", "south", "west", "drop"]):
            return jsonify({'message': 'Not expected command'}), 404
        current_direction = robot.current_direction
        if (command == "drop"):
            new_direction = "center"
        else: 
            new_direction = changing_direction(current_direction, command)
       
        if (robot.role == True):
            {}
            #PAcket code goes there
    except Exception:
        return jsonify({'message': 'Invalid data'}), 404
    robot.move(new_direction)
    robot.save_to_db()
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
    try:
        token = request.headers.get('Authorization')
        payload = jwt.decode(token[7:])
        account_id = payload.get('sub')
        if (account_id == None):
            raise Exception

        account = Account.find_by_id(account_id)

        data = json.loads(request_data)
        current_location_x = data['x']
        current_location_y = data['y']
        current_direction = data['direction']

        robot = Robot(account_id, account.role, current_location_x, current_location_y, current_direction)
        robot.save_to_db()
    except Exception:
        return jsonify({'message': 'Invalid data'}),404
    response = robot.serialize
    return jsonify(response), 201