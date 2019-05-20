import aiPlacement as AI
import time

def fetch_user_input():
  # TODO: Listen to client if user input has been sent
  user_input = False
  if(user_input):
    return (1, 1)
  else:
    return (False, False)

def init_grid_layout(grid_width, grid_height):
  return ['empty'] * grid_width * grid_height

def init_robot_start_position(grid_layout, robot_nr, robot_pos, grid_width):
  updated_grid_layout = grid_layout

  x = robot_pos[0]
  y = robot_pos[1]
  direction = robot_pos[2]
  updated_grid_layout[x + y * grid_width] = 'robot' + str(robot_nr) + direction

  return updated_grid_layout


if __name__ == '__main__':
  # INIT
  # Position robot automatically moves back to after drop-off
  standard_pickup_position = (0, 0)

  # Grid
  grid_width = 6
  grid_height = 6
  grid_layout = init_grid_layout(grid_width, grid_height)

  # Check user input to change into manual mode
  # TODO: read user input
  manual_mode = False

  # Amount of robots
  # TODO: read user input for adding robot with starting position
  robots_initial_start_positions = [(0, 0, 'north'), (0, 2, 'east')]
  for index in range(0, len(robots_initial_start_positions)):
    grid_layout = init_robot_start_position(grid_layout, index, robots_initial_start_positions[index], grid_width)

  robots_goal_positions = [False, False]
  robots_drop_off_states = [True, True]
  robots_ready = [True, False]

  # ROBOT CALLS
  while True:
    if(not manual_mode):
      for robot_to_move in range(0, len(robots_ready)):
        if(robots_ready[robot_to_move] == False):
          break

        [Xuser, Yuser] = fetch_user_input()
        if Xuser and Yuser:
          goalPosition = (Xuser, Yuser)
        else:
          goalPosition = robots_goal_positions[robot_to_move]

        (nextAction, robotNextPosition, grid_layout, goalPosition) = AI.next_action_and_position_and_grid_update(grid_width, grid_height, grid_layout, goalPosition, robots_drop_off_states[robot_to_move], robot_to_move)
        print('nextAction', nextAction)
        print()
        print('##################')
        if(goalPosition == False and robots_drop_off_states[robot_to_move] == True):
          robots_goal_positions[robot_to_move] = standard_pickup_position
          robots_drop_off_states[robot_to_move] = False
        elif(goalPosition == False and robots_drop_off_states[robot_to_move] == False):
          robots_goal_positions[robot_to_move] = goalPosition
          robots_drop_off_states[robot_to_move] = True
        else:
          robots_goal_positions[robot_to_move] = goalPosition
        # robots_ready[robot_to_move] = False



    time.sleep(0.1)