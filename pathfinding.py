# ------------------------------------------------------------------------------
# Sample code from https://www.redblobgames.com/pathfinding/a-star/
# Copyright 2014 Red Blob Games <redblobgames@gmail.com>
#
# Feel free to use this code in your own projects, including commercial projects
# License: Apache v2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>
# ------------------------------------------------------------------------------


# Takes the gridlayout with the current obstacle positioning together with the start and goal position.
# Calculates the best path to the goal and returns the first action that needs to be taken to reach the goal
# as well as what position and direction the robot will end up in after that action.
# grid: Grid object
#       Example:
#         grid = Grid(numberOfxDimensions, numberOfyDimensions)
#         grid.obstacles = [(1, 3), (2, 3)]
#
# start: tuple, (xPosition, yPosition, xDirection, yDirection)
#       Example:
#         x = 1, y = 1
#         (x, y, 1, 0) means facing right
#         (x, y, -1, 0) left
#         (x, y, 0, 1) down
#         (x, y, 0, -1) up
#
# goal: tuple, (xPosition, yPosition)
#
# dropOff: boolean, True if robot holds a package and is going for a drop-off, False if robot is moving to pickup a package
#
# draw: boolean, True to display a printed representation of the grid. Default value set to False
#
# Output: tuple (string, tuple),
#         string: "pickup", "dropoff", "forward", "backward", "right", "left" or "wait" if no path to the goal was found
#         tuple: (xPosition, yPosition, cardinal direction)
#           Example:
#             ("right", (1, 1, "south"))
def robotNextActionAndPosition(grid, start, goal, dropOff, draw = False):
  if(goal == False):
    nextAction = 'wait'
    return (nextAction, start)

  goal = (goal[0], goal[1], 0, 0)
  came_from, cost_so_far = a_star_search(grid, start, goal, dropOff)
  pathList = actionList(came_from, start, goal, dropOff)

  if(draw):
    draw_grid(grid, pathList, start, goal, 4)

  nextAction = firstAction(pathList)
  if(nextAction == 'goal' and dropOff):
    nextAction = 'dropoff'
  elif(nextAction == 'goal' and not dropOff):
    nextAction = 'pickup'

  if(nextAction == False):
    nextAction = 'wait'
    return (nextAction, start)

  nextPos = nextPositon(pathList)
  return (nextAction, nextPos)


# Takes the gridlayout with the current obstacle positioning together with the start and goal position.
# Calculates if a path to the goal can be found and returns if there is a path of not.
# Input:
# grid: Grid object
#       Example:
#         grid = Grid(numberOfxDimensions, numberOfyDimensions)
#         grid.obstacles = [(1, 3), (2, 3)]
#
# start: tuple, (xPosition, yPosition, xDirection, yDirection)
#       Example:
#         x = 1, y = 1
#         (x, y, 1, 0) means facing right
#         (x, y, -1, 0) left
#         (x, y, 0, 1) down
#         (x, y, 0, -1) up
#
# goal: tuple, (xPosition, yPosition)
#
# dropOff: boolean, True if robot holds a package and is going for a drop-off, False if robot is moving to pickup a package
#
# Output: boolean, True if a path to the goal is possible, False if not
def existingPath(grid, start, goal, dropOff):
  goal = (goal[0], goal[1], 0, 0)
  came_from, cost_so_far = a_star_search(grid, start, goal, dropOff)
  pathList = actionList(came_from, start, goal, dropOff)
  return pathList != []

# ------------ HELPER FUNCTIONS BELOW ----------------------

def draw_tile(graph, x, y, path, width, start, goal):
  r = ""
  if(start[0] == x and start[1] == y):
    r = "A"

  if(path != True):
    for step in path:
      step = step[0]

      if(step[0] == x and step[1] == y):
        if step[2] == 1: r = r + ">"
        if step[2] == -1: r = r + "<"
        if step[3] == 1: r = r + "v"
        if step[3] == -1: r = r + "^"

  if(goal[0] == x and goal[1] == y):
    r = r + "Z"

  if (x, y) in graph.obstacles: r = "#"

  if(r == ""):
    r = "."
  return r

def draw_grid(graph, path, start, goal, width=2):
  for y in range(graph.height):
    for x in range(graph.width):
      print("%%-%ds" % width % draw_tile(graph, x, y, path, width, start, goal), end="")

    print()
  print('-----')

class SquareGrid:
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.obstacles = []

  def in_bounds(self, id):
    if(type(id[0]) is tuple):
      return 0 <= id[0][0] < self.width and 0 <= id[0][1] < self.height
    else:
      return 0 <= id[0] < self.width and 0 <= id[1] < self.height


  def passable(self, id):
    if(type(id[0]) is tuple):
      return (id[0][0], id[0][1]) not in self.obstacles
    else:
      return (id[0], id[1]) not in self.obstacles

  def front_clear(self, id):
    if(type(id[1][0]) is tuple):
      (xOrigin, yOrigin, xDirOrigin, yDirOrigin) = id[1][0]
    else:
      (xOrigin, yOrigin, xDirOrigin, yDirOrigin) = id[1]

    (xNew, yNew, xDirNew, yDirNew) = id[0][0]

    checkForward = (xNew + xDirNew, yNew + yDirNew)

    # Move forward
    if(xDirOrigin == xDirNew and yDirOrigin == yDirNew):
      # Activate below code to add restriction of package bumping into the side walls
      # return self.passable(checkForward) and self.in_bounds(checkForward)
      return self.passable(checkForward)

    # Turn
    else:
      checkDiagonal = (xNew + xDirNew + xDirOrigin, yNew + yDirNew + yDirOrigin)
      # Activate below code to add restriction of package bumping into the side walls
      # return self.passable(checkForward) and self.passable(checkDiagonal) and self.in_bounds(checkForward) and self.in_bounds(checkDiagonal)
      return self.passable(checkForward) and self.passable(checkDiagonal)

    return True

  def options(self, id):
    costForward = 2
    costBackward = 3
    costTurn = 2

    if(type(id[0]) is tuple):
      (x, y, xDir, yDir) = id[0]
    else:
      (x, y, xDir, yDir) = id
    if xDir == 1 and yDir == 0:
      # forward, backward, turn right, turn left
      results = [((x+1, y, xDir, yDir), costForward), ((x-1, y, xDir, yDir), costBackward), ((x, y, 0, 1), costTurn), ((x, y, 0, -1), costTurn)]

    elif xDir == -1 and yDir == 0:
      # forward, backward, turn right, turn left
      results = [((x-1, y, xDir, yDir), costForward), ((x+1, y, xDir, yDir), costBackward), ((x, y, 0, -1), costTurn), ((x, y, 0, 1), costTurn)]

    elif xDir == 0 and yDir == -1:
      # forward, backward, turn right, turn left
      results = [((x, y-1, xDir, yDir), costForward), ((x, y+1, xDir, yDir), costBackward), ((x, y, 1, 0), costTurn), ((x, y, -1, 0), costTurn)]

    elif xDir == 0 and yDir == 1:
      # forward, backward, turn right, turn left
      results = [((x, y+1, xDir, yDir), costForward), ((x, y-1, xDir, yDir), costBackward), ((x, y, -1, 0), costTurn), ((x, y, 1, 0), costTurn)]

    else:
      # False data, robot does not have a facing direction
      results = []

    results = filter(self.in_bounds, results)
    results = filter(self.passable, results)
    results_origin = list(map(lambda r: [r, id], results))
    results_origin = filter(self.front_clear, results_origin)
    results = map(lambda ro: ro[0], results_origin)
    return results

class Grid(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)

import heapq

class PriorityQueue:
  def __init__(self):
    self.elements = []

  def empty(self):
    return len(self.elements) == 0

  def put(self, item, priority):
    heapq.heappush(self.elements, (priority, item))

  def get(self):
    return heapq.heappop(self.elements)[1]


def heuristic(a, b):
  return abs(a[0] - b[0]) + abs(a[1] - a[1])

def a_star_search(graph, start, goal, dropOff):
  frontier = PriorityQueue()
  frontier.put(start, 0)
  came_from = {}
  cost_so_far = {}
  came_from[start] = None
  cost_so_far[start] = 0

  while not frontier.empty():
    current = frontier.get()

    if(dropOff):
      if(type(current[0]) is tuple):
        if current[0][0]+current[0][2] == goal[0] and current[0][1]+current[0][3] == goal[1]:
          break
      else:
        if(current[0]+current[2] == goal[0] and current[1]+current[3] == goal[1]):
          break
    else:
      if(type(current[0]) is tuple):
        if current[0][0] == goal[0] and current[0][1] == goal[1]:
          break
      else:
        if(current[0] == goal[0] and current[1] == goal[1]):
          break

    for next in graph.options(current):
      new_cost = cost_so_far[current] + next[1]
      if next not in cost_so_far or new_cost < cost_so_far[next]:
        cost_so_far[next] = new_cost
        priority = new_cost + heuristic(goal, next[0])
        frontier.put(next, priority)
        came_from[next] = current

  return came_from, cost_so_far

def findGoalAction(came_from, x, y, dropOff):
  for pos in came_from:
    if(dropOff):
      if(type(pos[0]) is tuple):
        if((pos[0][0] + pos[0][2], pos[0][1] + pos[0][3]) == (x, y)):
          return pos[0]
      else:
        if((pos[0] + pos[2], pos[1] + pos[3]) == (x, y)):
          return pos
    else:
      if(type(pos[0]) is tuple):
        if((pos[0][0], pos[0][1]) == (x, y)):
          return pos[0]
      else:
        if((pos[0], pos[1]) == (x, y)):
          return pos

  return False

def actionList(came_from, start, goal, dropOff):
  goalAction = findGoalAction(came_from, goal[0], goal[1], dropOff)
  if(goalAction == False):
    return list()
  elif(len(came_from) == 1):
    return 'goal'

  actions = list([(goalAction, 2)])
  keys = list(came_from.keys())

  if((goalAction, 2) in came_from):
    current = came_from[(goalAction, 2)]
  elif((goalAction, 3) in came_from):
    current = came_from[(goalAction, 3)]
  else:
    current = came_from[goalAction]

  while(current != start):
    actions.insert(0, current)
    current = came_from[current]

  actions.insert(0, (start, 2))
  return actions

def nextPositon(actionsList):
  if(actionsList == 'goal' or len(actionsList) == 1):
    return 'goal'
  (xNext, yNext, xDirNext, yDirNext) = actionsList[1][0]

  if(xDirNext == 1):
    return(xNext, yNext, 'east')
  elif(xDirNext == -1):
    return(xNext, yNext, 'west')
  elif(yDirNext == 1):
    return(xNext, yNext, 'south')
  elif(yDirNext == -1):
    return(xNext, yNext, 'north')

  return False

def firstAction(actionsList):
  goal = "goal"
  forward = "forward"
  backward = "backward"
  right = "right"
  left = "left"

  if(actionsList == 'goal' or len(actionsList) == 1):
    return goal
  elif(actionsList == []):
    return False

  (xCurrent, yCurrent, xDirCurrent, yDirCurrent) = actionsList[0][0]
  (xNext, yNext, xDirNext, yDirNext) = actionsList[1][0]


  # Forward or backward
  if(xDirCurrent == xDirNext and yDirCurrent == yDirNext):

    # Forward
    if((xCurrent + xDirCurrent, yCurrent + yDirCurrent) == (xNext, yNext)):
      return forward

    # Backward
    elif((xCurrent - xDirCurrent, yCurrent - yDirCurrent) == (xNext, yNext)):
      return backward

  # Right or left
  elif(xDirCurrent != xDirNext or yDirCurrent != yDirNext):

    # Facing up or down
    if(yDirCurrent != 0):

      # Right
      if((-1 * yDirCurrent, -1 * xDirCurrent) == (xDirNext, yDirNext)):
        return right

      # Left
      elif((yDirCurrent, xDirCurrent) == (xDirNext, yDirNext)):
        return left

    # Facing right or left
    elif(xDirCurrent != 0):

      # Right
      if((yDirCurrent, xDirCurrent) == (xDirNext, yDirNext)):
        return right

      # Left
      elif((-1 * yDirCurrent, -1 * xDirCurrent) == (xDirNext, yDirNext)):
        return left

  # No action taken
  return False