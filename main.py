from flask import Flask, Blueprint, request
from controller.tutor_controller import tutor
from controller.class_controller import classes
from controller.student_controller import student
import authentication.jwt_token_py as jwt
import json
from os import urandom
from authentication.login import login

app = Flask(__name__)
app.register_blueprint(tutor, url_prefix = '/tutor')
app.register_blueprint(classes, url_prefix = '/class')
app.register_blueprint(student, url_prefix = '/student')
app.register_blueprint(login, url_prefix = '/')

app.secret_key = urandom(24)

@app.route("/")
def hello():
    return "Welcome to Student Management System"

@app.route("/test")
def test():
    token = request.headers.get('Authorization')
    payload = jwt.decode(token[7:])
    return json.dumps(payload)


if __name__ == "__main__":
    app.run(host='0.0.0.0')

