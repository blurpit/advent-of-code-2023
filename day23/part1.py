import sys

from util import Graph

NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (-1, 0)
directions = [NORTH, EAST, SOUTH, WEST]

class ForestGraph(Graph):
    def get_neighbors(self, u, d=None):
        x, y = u
        for dx, dy in directions:
            if in_bounds(x + dx, y + dy):
                ch = grid[y + dy][x + dx]
                if ch == '#':
                    pass
                elif ch == '.':
                    yield (x + dx, y + dy), 1
                else:
                    if ch == '^':
                        dir2 = NORTH
                    elif ch == '>':
                        dir2 = EAST
                    elif ch == 'v':
                        dir2 = SOUTH
                    elif ch == '<':
                        dir2 = WEST
                    yield (x + dx + dir2[0], y + dy + dir2[1]), 2

def in_bounds(x, y):
    return 0 <= x < width and 0 <= y < height

def print_grid():
    for row in grid:
        print(row)
    print()

if __name__ == '__main__':
    with open('input.txt') as file:
        grid = [line.strip() for line in file.readlines()]
        width = len(grid[0])
        height = len(grid)

        start = (1, 0)
        end = (width-2, height-1)

        graph = ForestGraph()
        sys.setrecursionlimit(3000) # lol
        topo_order = graph.topo_sort_wfs(start)

        longest_paths = {}
        marked = set()
        for u in topo_order:
            marked.add(u)
            for v, cost in graph.get_neighbors(u):
                if v not in marked:
                    longest_paths[v] = max(
                        longest_paths.get(v, 0),
                        longest_paths.get(u, 0) + cost
                    )
        print(longest_paths[end])
