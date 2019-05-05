from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, join, select
from sqlalchemy.sql import select
import MySQLdb
from flask import Flask, Blueprint
from flask import request
import json
from sqlalchemy.orm import sessionmaker
import authentication.login as login
#from authentication.login import role_authorized
import authentication.jwt_token_py as jwt
classes = Blueprint('classes',__name__)
#classes.register_blueprint(login, url_prefix = '/login')
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

enrol = Table('enrollments', meta, autoload=True,
                           autoload_with=engine)

e = enrol.select()
result = conn.execute(e)

enrol_list_temp = json.dumps([dict(r) for r in result])
enrol_list = json.loads(enrol_list_temp)

students = Table('account', meta, autoload=True,
                           autoload_with=engine)

s = students.select()
result = conn.execute(s)

student_list_temp = json.dumps([dict(r) for r in result])
student_list = json.loads(student_list_temp)

@classes.route("/create", methods = ['POST'])
@role_authorized('tutor')
def create_class():
   request_data = request.get_data()
   try:
      class_data = json.loads(request_data)
      token = request.headers.get('Authorization')
      payload = jwt.decode(token[7:])
      class_tutor = payload.get('sub')
      class_name = class_data['name']
      class_limit = class_data['limit']

      if ((class_limit < 0) or (class_limit > 15)):
         return json.dumps({'message': 'Limitation must between 0 and 15'}), 400 

      if ((class_tutor == None) or (len(class_name) == 0) or (class_limit == None)):
         raise Exception
   except Exception:
      return json.dumps({'message': 'Invalid class data'}), 400 
   ins = classes_tab.insert(None).values(tutor_id = class_tutor, name = class_name, student_limit = class_limit, current_enrolled = 0, status = True)  
   conn = engine.connect()
   conn.execute(ins)
   return "Successful" 

@classes.route("/update", methods = ['PUT'])
@role_authorized('tutor')
def update_class():
   request_data = request.get_data()
   try:
      class_data = json.loads(request_data)
      class_id = class_data['id']
      class_name = class_data['name']
      class_limit = class_data['limit']
      flag = False
         
      if ((class_id == None) or ((len(class_name) == 0) and (class_limit == None))):
         raise Exception

              
      for c in class_list:
         if c['id'] == class_id:
            if c['student_limit'] < class_limit:
               return json.dumps({'message': 'Student limit must not decrease'}), 400
            else: flag = True
      
      if flag == False:
         return json.dumps({'message': 'Class not found'}), 400

   except Exception:
      return json.dumps({'message': 'Invalid class data'}), 400
   upt = classes_tab.update(None).where(classes_tab.c.id == class_id).values(name=class_name, student_limit = class_limit)
   conn = engine.connect()
   conn.execute(upt)
   return "Succesful"
  
@classes.route("/delete", methods = ['DELETE'])
@role_authorized('tutor')
def delete_class():
    request_data = request.get_data()
    try:
       class_data = json.loads(request_data)
       class_id = class_data['id']
       flag = False
       if ((class_id == None)):
          raise Exception

       for c in class_list:
          if c['id'] == class_id:
             flag = True
     
       if flag == False:
          return json.dumps({'message': 'Class not found'}), 400

    except Exception:
       return json.dumps({'message': 'Invalid class data'}), 400
    det = classes_tab.update(None).where(classes_tab.c.id == class_id).values(status = False)
    conn = engine.connect()
    conn.execute(det)
    return "Succesful"

@classes.route("/list", methods = ['GET'])
@role_authorized('tutor')
def list_class():
    try:
       token = request.headers.get('Authorization')
       payload = jwt.decode(token[7:])
       tutor_id = payload.get('sub')
       if ((tutor_id == None)):
          raise Exception
    except Exception:
       return json.dumps({'message': 'Invalid class data'}), 400
    s = classes_tab.select().where(classes_tab.c.tutor_id == tutor_id)
    conn = engine.connect()
    result = conn.execute(s)

    return json.dumps([dict(r) for r in result])

@classes.route("/students", methods = ['GET'])
@role_authorized('tutor')
def list_student():
    request_data = request.get_data()
    try:
       class_data = json.loads(request_data)
       class_ID = class_data['id']
       valid_class = False
       if ((class_ID == None)):
          raise Exception

       for c in class_list:
          if c['id'] == class_ID:
             valid_class = True

       if valid_class == False:
          return json.dumps({'message': 'Class not exist'}), 400
    except Exception:
       return json.dumps({'message': 'Invalid class data'}), 400
    s = select([students.c.name, enrol.c.registered]).where((enrol.c.class_id == class_ID) and (students.c.id == enrol.c.student_id))
    result = conn.execute(s)
    
    return json.dumps([dict(r) for r in result])

@classes.route("/remove", methods = ['PUT'])
@role_authorized('tutor')
def remove_student():
    request_data = request.get_data()
    try:
       class_data = json.loads(request_data)
       class_ID = class_data['id']
       student_id = class_data['student']

       valid_class = False
       valid_student = False
       valid_enrol = False

       if ((class_ID == None) or (student_id == None)):
          raise Exception

       for c in class_list:
          if c['id'] == class_ID:
             valid_class = True

       for s in student_list:
          if s['id'] == student_id:
             valid_student = True

       for e in enrol_list:
          if ((e['class_id'] == class_ID) and (e['student_id'] == student_id) and (e['registered'] == True)):
             valid_enrol = True
      
       if ((valid_class == False) or (valid_enrol == False) or (valid_student == False)):
          return json.dumps({'message': 'Student and class must be valid and not removed before'}), 400

    except Exception:
       return json.dumps({'message': 'Invalid data'}), 400
    upt = classes_tab.update(None).where(classes_tab.c.id == class_ID).values(current_enrolled = classes_tab.c.current_enrolled - 1 )
    conn = engine.connect()
    conn.execute(upt)
    upt = enrol.update(None).where((enrol.c.class_id == class_ID) and (enrol.c.student_id == student_id)).values(registered = False)
    conn.execute(upt)
    return "Succesful"

  