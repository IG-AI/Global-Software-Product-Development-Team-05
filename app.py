from flask import Flask, jsonify
from flask_cors import CORS

from db import DB

from controller.robot_controller import robots
from controller.account_controller import accounts
from authentication.login import login

app = Flask(__name__)
app.config.from_object('config.Config')

app.register_blueprint(robots)
app.register_blueprint(accounts)
app.register_blueprint(login)

cors = CORS(send_wildcard=True)
cors.init_app(app)

if __name__ == '__main__':
    DB.init_app(app)
    with app.app_context():
        DB.create_all()
    app.debug = True
    app.run(host='127.0.0.1', port=5000)