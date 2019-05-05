from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select
import MySQLdb
from flask import Flask, Blueprint
from flask import request
import json
import authentication.jwt_token_py as jwt
from authentication.login import role_authorized
from sqlalchemy.orm import sessionmaker
student = Blueprint('student',__name__)
engine = create_engine('mysql://root@127.0.0.1:3306/project', echo = True)
conn = engine.connect()
meta = MetaData()
Session = sessionmaker(bind = engine)
session = Session()

classes_tab = Table('classes', meta, autoload=True,
                           autoload_with=engine)

c = classes_tab.select()
result = conn.execute(c)

class_list_temp = json.dumps([dict(r) for r in result])
class_list = json.loads(class_list_temp)

students = Table('account', meta, autoload=True,
                           autoload_with=engine)

s = students.select()
result = conn.execute(s)

student_list_temp = json.dumps([dict(r) for r in result])
student_list = json.loads(student_list_temp)

enrol = Table('enrollments', meta, autoload=True,
                           autoload_with=engine)

e = enrol.select()
result = conn.execute(e)

enrol_list_temp = json.dumps([dict(r) for r in result])
enrol_list = json.loads(enrol_list_temp)

@student.route("/create", methods = ['POST'])
def create_student():
    request_data = request.get_data()
    try:
       student_data = json.loads(request_data)
       student_name = student_data['name']

       if ((len(student_name) < 3) or (len(student_name) > 50)):
          return json.dumps({'message': 'Length of username must between 3 and 50 character'}), 400
      
       student_email = student_data['email']

       if len(student_email) < 3:
          return json.dumps({'message': 'Length of email must be greater than 3 character'}), 400 
       
       for s in student_list:
          if s['email'] == student_email:
             return json.dumps({'message': 'Duplicated email'}), 400 

       student_password = student_data['password']

       if ((len(student_password) < 5) or (len(student_password) >10) or (' ' in student_password) or (any(c.isdigit() for c in student_password) == False)):
          return json.dumps({'message':'Password must be between 5 and 10 character, no space and at least a number'}), 400

       hashed_pass = jwt.hash(student_password)
       if ((len(student_name) == 0) or (len(student_email) == 0) or (len(student_password) == 0) ):
          raise Exception
    except Exception:
       return json.dumps({'message': 'Invalid account data'}), 400 
    ins = students.insert(None).values(role = 'student', name = student_name, email = student_email, password = hashed_pass)  
    conn.execute(ins)
    return "Successful"

@student.route("/enrol", methods = ['POST'])
@role_authorized('student')
def enrol_student():
    request_data = request.get_data()
    try:
       enrol_data = json.loads(request_data)
       token = request.headers.get('Authorization')
       payload = jwt.decode(token[7:])
       student_id = payload.get('sub')
       class_id = enrol_data['class']

       if ((student_id == None) or (class_id == None)):
          raise Exception

       for e in enrol_list:
          if ((e['class_id'] == class_id) and (e['student_id'] == student_id)):
             return json.dumps({'message': 'Student who once been remove can not enroll again'}), 400 
    except Exception:
       return json.dumps({'message': 'Invalid account data'}), 400 
    upt = classes_tab.update(None).where(classes_tab.c.id == class_id).values(current_enrolled = classes_tab.c.current_enrolled + 1 )
    conn.execute(upt)
    ins = enrol.insert(None).values(class_id = class_id, student_id = student_id, registered = True)  
    conn.execute(ins)
    return "Successful"

@student.route("/deregister", methods = ['PUT'])
@role_authorized('student')
def deregister_student():
    request_data = request.get_data()
    try:
       class_data = json.loads(request_data)
       class_ID = class_data['id']

       token = request.headers.get('Authorization')
       payload = jwt.decode(token[7:])
       student_id = payload.get('sub')

       valid_class = False
       valid_enrol = False

       if ((class_ID == None) or (student_id == None)):
          raise Exception
      
       for c in class_list:
          if c['id'] == class_ID:
             valid_class = True
       
       for e in enrol_list:
          if ((e['class_id'] == class_ID) and (e['registered'] == True)):
             valid_enrol = True
       
       if ((valid_class == False) or (valid_enrol == False)):
          return json.dumps({'message': 'Student and class must be valid and not removed before'}), 400

    except Exception:
       return json.dumps({'message': 'Invalid class data'}), 400
    upt = classes_tab.update(None).where(classes_tab.c.id == class_ID).values(current_enrolled = classes_tab.c.current_enrolled - 1 )
    conn.execute(upt)
    upt = enrol.update(None).where((enrol.c.class_id == class_ID) and (enrol.c.student_id == student_id)).values(registered = False)
    conn.execute(upt)
    return "Succesful"

@student.route("/class", methods = ['GET'])
@role_authorized('student')
def list_class():
    try:
       token = request.headers.get('Authorization')
       payload = jwt.decode(token[7:])
       student_ID = payload.get('sub')
       if ((student_ID == None)):
          raise Exception
    except Exception:
       return json.dumps({'message': 'Invalid class data'}), 400
    s = select([classes_tab.c.name, classes_tab.c.student_limit, classes_tab.c.current_enrolled, classes_tab.c.status]).where((classes_tab.c.id == enrol.c.class_id) and (enrol.c.student_id == student_ID))
    result = conn.execute(s)

    return json.dumps([dict(r) for r in result])
    

