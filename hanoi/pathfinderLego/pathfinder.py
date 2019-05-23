from pathfinder.maze import create_maze
from pathfinder.algorithm import fill_shortest_path, backtrack_to_start

def convert_path(path):
    path.reverse()
    steps = []
    step = ''
    for i in range(0, len(path) - 1):
        if ((path[i][0] == path[i+1][0]) and (path[i][1] == path[i+1][1] - 1)):
            step = 'north'
            steps.append(step)
        elif ((path[i][0] == path[i+1][0]) and (path[i][1] == path[i+1][1] + 1)):
            step = 'south'
            steps.append(step)
        elif ((path[i][0] == path[i+1][0] + 1) and (path[i][1] == path[i+1][1])):
            step = 'west'
            steps.append(step)
        elif ((path[i][0] == path[i+1][0] - 1) and (path[i][1] == path[i+1][1])):
            step = 'east'
            steps.append(step)
    steps.append('pack')
    return steps


E = 'E R O E E\nE E O G E\nE E O E E\nE E E E E'

def find_path(E):

    maze = create_maze(E)
    if maze == None:
        return None
    filled = fill_shortest_path(maze.board, maze.start, maze.end)
    path = backtrack_to_start(filled, maze.end)
    steps = convert_path(path)
    print(path)
    print(steps)
    return steps

#Invert path
#Convert to absolute direction

#print(path)
#print(steps)
if __name__ == "__main__":
    find_path(E)