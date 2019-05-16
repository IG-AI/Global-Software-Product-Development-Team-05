import pathfinding as pf

if __name__ == '__main__':
  start, goal = (0, 0, 0, 1), (5, 4, 0, 0)
  grid = pf.Grid(6, 6)
  grid.obstacles = [(5, 5), (2, 5), (2, 3), (4, 3), (0, 4), (1, 3), (4, 2), (1, 2), (5, 2)]

  print("First action:", pf.robotNextAction(grid, start, goal))

  came_from, cost_so_far = pf.a_star_search(grid, start, goal)
  pathList = pf.actionList(came_from, start, goal)
  pf.draw_grid(grid, path=pathList, start=start, goal=goal, width=4)
