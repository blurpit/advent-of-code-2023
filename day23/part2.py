from util import Graph

NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (-1, 0)
directions = [NORTH, EAST, SOUTH, WEST]

def build_graph():
    """ build a graph of only the junctions """
    g = Graph()

    # build graph with every space as a vertex
    for y in range(height):
        for x in range(width):
            if grid[y][x] != '#':
                for dx, dy in directions:
                    if in_bounds(x + dx, y + dy):
                        if grid[y + dy][x + dx] != '#':
                            g.add_edge((x, y), (x + dx, y + dy), 1)

    # remove vertices that are not junctions
    # eg. u <-3-> v <-4-> w becomes u <-7-> w
    for v in g.vertices:
        nbrs = g.get_neighbors(v)
        if len(nbrs) == 2:
            g.delete_vertex(v)
            (u, c1), (w, c2) = nbrs
            g.add_edge(u, w, c1 + c2)
            g.add_edge(w, u, c1 + c2)

    return g

def longest_path(g, start, end):
    return longest_path_dfs(g, start, end, 0, set())

def longest_path_dfs(g, u, end, path_len, marked):
    """ Use DFS backtracking to try every path and return the length of the longest one """
    if u == end: # base case (path is complete)
        global paths
        if path_len > paths:
            paths = path_len
            print('New max:', path_len)
        return path_len

    marked.add(u)
    max_len = 0
    for v, cost in g.get_neighbors(u):
        if v not in marked:
            max_len = max(
                max_len,
                longest_path_dfs(g, v, end, path_len + cost, marked)
            )
    marked.remove(u) # backtrack
    return max_len

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

        graph = build_graph()
        print(graph)
        paths = 0
        print('Answer:', longest_path(graph, start, end))
