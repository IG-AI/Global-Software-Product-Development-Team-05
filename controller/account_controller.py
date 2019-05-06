from flask import Flask, Blueprint, jsonify
from flask import request
import json
#from sqlalchemy.orm import sessionmaker

import authentication.login as login
from authentication.login import pre_authorized
import authentication.jwt_token_py as jwt
#from model.robot import Robot
from model.account import Account
#from util.direction import changing_direction

accounts = Blueprint('account',__name__)

@accounts.route("/create", methods = ['POST'])
def create_account():
   robot_accounts = Account.query.all()
   #robot_temp = json.dumps([dict(r) for r in robot_accounts])
   #robot_accounts = json.loads(robot_temp)
   request_data = request.get_data()
   try:
      account_data = json.loads(request_data)
      username = account_data['username']      
      role = account_data['role']
      password = account_data['password']

      if((username == None) or (role == None) or (password == None)):
         raise Exception
       
      for account in robot_accounts:
         account = account.serialize
         if (account['username'] == username):
            return json.dumps({'message': 'Duplicated username'}), 400 

      hashed_pass = jwt.hash(password)
      account = Account(role, username, hashed_pass)
      account.save_to_db()
   except Exception:
      return json.dumps({'message': 'Invalid account data'}), 400 
   return "Successful"