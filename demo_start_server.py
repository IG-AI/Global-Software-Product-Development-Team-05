from time import sleep
import util.pathfinding as pf

from model.server import Server

server = Server(host="10.10.10.2")
server.connect()

start, goal = (0, 0, 0, 1), (5, 4)
grid = pf.Grid(6, 6)
grid.obstacles = [(5, 5), (2, 5), (2, 3), (4, 3), (0, 4), (1, 3), (4, 2), (1, 2), (5, 2)]
server.set_map(grid)
startFlag = False
while True:
    sleep(1)
    if (len(server.robots) > 0) & (startFlag == False):
        server.start_robot(server.robots[0])
        startFlag = True