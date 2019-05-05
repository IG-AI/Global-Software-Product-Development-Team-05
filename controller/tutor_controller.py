from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import MySQLdb
from flask import Flask, Blueprint
from flask import request
import json
import string
import authentication.jwt_token_py as jwt
from authentication.login import role_authorized
tutor = Blueprint('tutor',__name__)
engine = create_engine('mysql://root@127.0.0.1:3306/project', echo = True)
meta = MetaData()

tutors = Table('account', meta, autoload=True,
                           autoload_with=engine)

t = tutors.select()
conn = engine.connect()
result = conn.execute(t)

tutor_list_temp = json.dumps([dict(r) for r in result])
tutor_list = json.loads(tutor_list_temp)

@tutor.route("/tutors", methods = ['GET'])
def hello_tutors():
    return "Hello"

@tutor.route("/create", methods = ['POST'])
@role_authorized('admin')
def create_tutors():
    request_data = request.get_data()
    try:
       tutor_data = json.loads(request_data)
       tutor_name = tutor_data['name']

       if ((len(tutor_name) < 3) or (len(tutor_name) > 50)):
          return json.dumps({'message': 'Length of username must between 3 and 50 character'}), 400
      
       tutor_email = tutor_data['email']

       if len(tutor_email) < 3:
          return json.dumps({'message': 'Length of email must be greater than 3 character'}), 400 
       
       for t in tutor_list:
          if t['email'] == tutor_email:
             return json.dumps({'message': 'Duplicated email'}), 400 

       tutor_password = tutor_data['password']

       if ((len(tutor_password) < 5) or (len(tutor_password) >10) or (' ' in tutor_password) or (any(c.isdigit() for c in tutor_password) == False)):
          return json.dumps({'message':'Password must be between 5 and 10 character, no space and at least a number'}), 400

       hashed_pass = jwt.hash(tutor_password)

       if ((len(tutor_name) == 0) or (len(tutor_email) == 0) or (len(tutor_password) == 0) ):
          raise Exception
    except Exception:
       return json.dumps({'message': 'Invalid account data'}), 400 
    ins = tutors.insert(None).values(role = 'tutor', name = tutor_name, email = tutor_email, password = hashed_pass)  
    conn = engine.connect()
    conn.execute(ins)
    return "Successful"
  