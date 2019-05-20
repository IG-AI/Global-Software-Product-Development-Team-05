from flask import Flask, jsonify
from flask_cors import CORS

from db import DB

from controller.robot_controller import robots
from controller.account_controller import accounts
from controller.lego_controller import legos
from authentication.login import login

app = Flask(__name__)
CORS(app)
app.config.from_object('config.Config')

app.register_blueprint(robots)
app.register_blueprint(accounts)
app.register_blueprint(login)
app.register_blueprint(legos)

#cors = CORS(send_wildcard=True)
#cors.init_app(app)

if __name__ == '__main__':
    #global map
    DB.init_app(app)
    with app.app_context():
        DB.create_all()
    app.debug = True
    app.run(host='0.0.0.0', port=5000)