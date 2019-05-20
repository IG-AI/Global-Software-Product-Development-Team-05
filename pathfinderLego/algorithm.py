import pathfinder.maze as maze
import math

def fill_shortest_path(board, start, end, max_distance = math.inf):
    nboard = board.clone()
    nboard.clear_count(math.inf)

    open_list = [start]
    nboard.at(start).count = 0

    neighbours = [[-1,0], [1,0], [0,-1], [0,1]]
    while open_list:
        cur_pos = open_list.pop(0)
        cur_cell = nboard.at(cur_pos)

        for neighbour in neighbours:
            ncell_pos = maze.add_point(cur_pos,neighbour)
            if not nboard.is_valid_point(ncell_pos):
                continue

            cell = nboard.at(ncell_pos)

            if cell.type != maze.CellType.Empty:
                continue

            dist = cur_cell.count + 1
            if dist > max_distance:
                continue

            if cell.count > dist:
                cell.count = dist
                cell.path_from = cur_cell
                cell.pos = ncell_pos
                open_list.append(ncell_pos)

    return nboard

def backtrack_to_start(board, end):
    cell = board.at(end)
    path = []
    while cell!= None:
        path.append(cell.pos)
        cell = cell.path_from

    return path