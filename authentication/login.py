from flask import  Flask, jsonify, request, Blueprint, session, redirect, url_for
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from functools import wraps
from os import urandom
import json
import authentication.jwt_token_py as jwt
#from controller.student_controller import student
login = Blueprint('login',__name__)
engine = create_engine('mysql://root@127.0.0.1:3306/project', echo = True)
meta = MetaData()
login.secret_key = urandom(24)

#students = Table('account', meta, autoload=True,
                           #autoload_with=engine)

#accounts = []
robot_accounts = {}
with open('authentication/robot_accounts.json') as f:
    robot_accounts = json.load(f)

#s = students.select()
#conn = engine.connect()
#result = conn.execute(s)

#accounts_temp = json.dumps([dict(r) for r in result])
#accounts = json.loads(accounts_temp)

@login.route('/login', methods=['POST'])
def signin():
    try:
        data = request.get_json(silent=True)
        username = data.get("username")
        password = data.get("password")

        #for admin in admin_accounts:
            #if (username == admin['username'] and password == admin['password']):
                #return jsonify({"success": True, 
                        #"token": jwt.encode(admin)}), 200

        for account in robot_accounts:
            hashed = account['password']
            payload = jwt.decode(hashed)
            pass_stored = payload.get('sub')
            if (username == account['name'] and password == pass_stored):
                session['username'] = True
                return jsonify({"success": True, 
                         "token": jwt.encode(account)}), 200

        return jsonify({"success": False, 
                 "message": "Wrong username or password"}), 403
    except Exception:
        return jsonify({"success": False, 
                        "message": "Bad request"}), 400

@login.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('admin')
   return redirect(url_for('hello'))

@login.route('/clear')
def clear():
    session.clear()
    return redirect(url_for('hello'))


#def role_authorized(str):
def pre_authorized(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            payload = jwt.decode(token[7:])

            if payload is None:
                return jsonify({"success": False, 
                        "message": "Unauthorized"}), 403

            account_id = payload.get('sub')

            for robot in robot_accounts:
                if ((account_id == robot['id'])):
                    return f(*args, **kwargs)

                #for a in accounts:
                    #if ((account_id == a['id']) and (a['role'] == str)):
                        #return f(*args, **kwargs)

            return jsonify({"success": False, 
                    "message": "Unauthorized"}), 403
        except Exception:
            return jsonify({"success": False, 
                        "message": "Bad request"}), 400
    return decorated
    #return pre_authorized

    