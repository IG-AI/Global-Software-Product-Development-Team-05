from flask import Flask
from flask_cors import CORS

#from controllers.auth import auth_bp
#from controllers.packet import packet_bp
#from controllers.user import user_bp
#from controllers.shelf import shelf_bp
#from controllers.job import job_bp
#from controllers.robot import robot_bp

app = Flask(__name__)
app.config.from_object('config.Config')

#app.register_blueprint(auth_bp)
#app.register_blueprint(packet_bp)
#app.register_blueprint(user_bp)
#app.register_blueprint(shelf_bp)
#app.register_blueprint(robot_bp)
#app.register_blueprint(job_bp)

cors = CORS(send_wildcard=True)
cors.init_app(app)


if __name__ == '__main__':
    from db import recreate_database
    recreate_database()
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
