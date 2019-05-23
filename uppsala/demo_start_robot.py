from model.robot_demo import Robot


robot = Robot(current_location_x=0, current_location_y=0, current_direction="north", server_ip='127.0.0.1', server_port=2526)
robot.connect()
robot.start()
