import pathfinding as pf

# Global variables
robot_identifier = 'robot'
north_identifier = 'north'
south_identifier = 'south'
east_identifier = 'east'
west_identifier = 'west'
empty_identifier = 'empty'
package_identifier = 'package'

# Function: next_action_and_position_and_grid_update
# Inputs current grid and which robots that moves and selects where to place the package and
# returns the next action the robot needs to take, the position and direction of the robot after that
# action as well as an updated grid layout.
#
# Input:
#   grid_width: int, width of the grid
#   grid_height: int, height of the grid
#   current_grid_layout: array[string], status of each grid positon, see global variables for valid strings
#               example (6x6 grid):
#                   ['robot1north', 'empty', 'empty', 'empty', 'empty', 'empty',
#                     'empty', 'empty', 'empty', 'empty', 'empty', 'empty',
#                     'empty', 'empty', 'empty', 'empty', 'empty', 'empty',
#                     'robot2east', 'empty', 'empty', 'empty', 'empty', 'empty',
#                     'empty', 'empty', 'empty', 'empty', 'empty', 'empty',
#                     'empty', 'empty', 'empty', 'package', 'package', 'package']
#   goalPosition: tuple(int, int), coordinates for the goal position (xPosition, yPosition).
#                 If goal position (False, False) is inputed the next drop-off location is automatically selected.
#   dropOff: boolean, True if robot holds a package and is going for a drop-off, False if robot is moving to pickup a package
#
#   robot_nr: int, id of the robot that wants to be moved. Default set to 1
#
# Return:
#   nextAction: string, "pickup", "dropoff", "forward", "backward", "right", "left" or "wait" if no path to the goal was found
#   robotNextPosition: tuple, (xPosition, yPosition, cardinal direction)
#                      cardinal directions: "north", "east", "south", "west"
#                         Example:
#                          (1, 1, "south")
#   new_grid_layout: array[string]: updated version of input current_grid_layout where the next action of the robot has been added
#
#   goalPosition: tuple, (xPosition, yPosition). The function may or may not update the goal positon depending on the input
def next_action_and_position_and_grid_update(grid_width, grid_height, current_grid_layout, goalPosition, dropOff, robot_nr = 0):
  draw = True

  grid = pf.Grid(grid_width, grid_height)
  currentRobotPosition = get_robot_position(current_grid_layout, grid.width, grid.height, robot_nr)
  grid.obstacles = mark_obstacles(current_grid_layout, grid.width, grid.height, (currentRobotPosition[0], currentRobotPosition[1]))

  if(goalPosition == False):
    goalPosition = next_package_position(grid, current_grid_layout, grid.width, grid.height, currentRobotPosition, dropOff)

  (nextAction, robotNextPosition) = pf.robotNextActionAndPosition(grid, currentRobotPosition, goalPosition, dropOff, draw)

  if(nextAction == 'wait'):
    new_grid_layout = current_grid_layout
  else:
    new_grid_layout = updated_grid_layout(current_grid_layout, grid.width, currentRobotPosition, robotNextPosition, nextAction, goalPosition, robot_nr)

  if(nextAction == 'pickup' or nextAction == 'dropoff'):
    goalPosition = False

  return (nextAction, robotNextPosition, new_grid_layout, goalPosition)


# ------------ HELPER FUNCTIONS BELOW ----------------------


def next_package_position(grid, grid_layout, width, height, currentRobotPosition, dropOff):
  for y in list(reversed(list(range(0, height)))):
    for x in list(reversed(list(range(0, width)))):
      goal = (x, y)
      if(grid_layout[x + y * width] == empty_identifier and pf.existingPath(grid, currentRobotPosition, goal, dropOff)):
        return goal

  return False

def mark_obstacles(grid_layout, width, height, robot_position):
  notConsideredObstacle = [empty_identifier]
  obstacleList = list()

  # Loops through all x and y positions
  for y in range(0, height):
    for x in range(0, width):

      # Only checks if it is a position where the robot is not standing on
      if((x, y) != robot_position):
        currentPos = grid_layout[x + y * width]

        # If the current position is considered an obstacle it gets added to the obstacle list
        if(currentPos not in notConsideredObstacle):
          obstacleList.append((x, y))

  return obstacleList

def get_robot_position(grid_layout, width, height, robot_nr = 0):
  for y in range(0, height):
    for x in range(0, width):
      currentPos = grid_layout[x + y * width]

      # If the position has the robot
      if(robot_identifier in currentPos and str(robot_nr) in currentPos):

        # If robot is facing North
        if(north_identifier in currentPos):
          return (x, y, 0, -1)

        # If robot is facing South
        elif(south_identifier in currentPos):
          return (x, y, 0, 1)

        # If robot is facing East
        elif(east_identifier in currentPos):
          return (x, y, 1, 0)

        # If robot is facing West
        elif(west_identifier in currentPos):
          return (x, y, -1, 0)

  return False

def updated_grid_layout(old_grid_layout, gridWidth, currentRobotPosition, nextRobotPosition, nextAction, goalPosition, robot_nr = 0):
  new_grid_layout = old_grid_layout
  if(nextAction == 'dropoff'):
    (goalX, goalY) = goalPosition
    new_grid_layout[goalX + goalY * gridWidth] = package_identifier
  elif(nextAction == 'pickup'):
    return old_grid_layout
  else:
    currentX = currentRobotPosition[0]
    currentY = currentRobotPosition[1]
    newX = nextRobotPosition[0]
    newY = nextRobotPosition[1]
    newDirection = nextRobotPosition [2]
    new_grid_layout[currentX + currentY * gridWidth] = empty_identifier
    new_grid_layout[newX + newY * gridWidth] = robot_identifier + str(robot_nr) + newDirection

  return new_grid_layout

def init_grid_layout(grid_width, grid_height):
  return ['empty'] * grid_width * grid_height

def init_robot_start_position(grid_layout, robot_nr, robot_pos, grid_width):
  updated_grid_layout = grid_layout

  x = robot_pos[0]
  y = robot_pos[1]
  direction = robot_pos[2]
  updated_grid_layout[x + y * grid_width] = 'robot' + str(robot_nr) + direction

  return updated_grid_layout