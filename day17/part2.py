from math import inf

from util import Graph

NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (-1, 0)
directions = [NORTH, EAST, SOUTH, WEST]
dir_names = ['NORTH', 'EAST', 'SOUTH', 'WEST']

def build_graph():
    # See the comment under part1 / build_graph(). This is the same, except instead of doing
    # steps 1 through 3, it does 1 through 10, and only adds left/right turns on steps 4-10.
    g = Graph()
    for y in range(height):
        for x in range(width):
            # print(f'({x}, {y})')
            for dir_i in range(len(directions)):
                # print(f'\t{dir_names[dir_i]}')
                # Add edges 3 steps forward, incrementing direction counts
                u = (x, y, 0, 0, 0, 0)
                for steps in range(1, 11):
                    # print(f'\t\t{steps} steps')
                    # Add edge forward
                    # u = make_vertex(x, y, dir_i, steps-1)
                    v = make_vertex(x, y, dir_i, steps)
                    if in_bounds(v):
                        # print(f'\t\t\tFORWARD\t{u} -> {v}')
                        g.add_edge(u, v, heat_loss(v))

                    # Add edges to the 'left' and 'right' of v that reset the direction counts
                    if steps >= 4:
                        vx, vy, *_ = v
                        dir_left = (dir_i + 3) % 4
                        w = make_vertex(vx, vy, dir_left, 1)
                        if in_bounds(w):
                            # print(f'\t\t\tLEFT\t{v} -> {w}')
                            g.add_edge(v, w, heat_loss(w))

                        dir_right = (dir_i + 1) % 4
                        w = make_vertex(vx, vy, dir_right, 1)
                        if in_bounds(w):
                            # print(f'\t\t\tRIGHT\t{v} -> {w}')
                            g.add_edge(v, w, heat_loss(w))

                    u = v
            # print()
    return g

def make_vertex(x, y, dir_i, steps):
    dx, dy = directions[dir_i]
    v = [
        x + dx * steps,
        y + dy * steps,
        0, 0, 0, 0
    ]
    v[dir_i + 2] = steps
    return tuple(v)

def in_bounds(v):
    x, y, *_ = v
    return 0 <= x < width and 0 <= y < height

def heat_loss(v):
    x, y, *_ = v
    return grid[y][x]

def parse_grid(text):
    grid = text.splitlines()
    for y, line in enumerate(grid):
        grid[y] = [int(ch) for ch in line.strip()]
    return grid

def print_path(path):
    grid2 = [
        ['.' for x in range(width)]
        for y in range(height)
    ]
    if path:
        u = path[0]
        grid2[u[1]][u[2]] = 's'

        for v in path[1:]:
            (ux, uy, *_) = u
            (vx, vy, *_) = v
            direction = (vx - ux, vy - uy)
            if direction == NORTH:
                grid2[vy][vx] = '^'
            elif direction == EAST:
                grid2[vy][vx] = '>'
            elif direction == SOUTH:
                grid2[vy][vx] = 'v'
            elif direction == WEST:
                grid2[vy][vx] = '<'
            u = v

    for row in grid2:
        print(''.join(row))
    print()

if __name__ == '__main__':
    with open('input.txt') as file:
        grid = parse_grid(file.read())
        width = len(grid[0])
        height = len(grid)

        print('Building graph...')
        graph = build_graph()
        print(f'V={graph.num_vertices()} E={graph.num_edges()}')

        print('Running dijkstra...')
        dist, pred = graph.dijkstra((0, 0, 0, 0, 0, 0))

        print('Finding shortest path...')
        answer = inf
        min_v = None
        for dir_i in range(4):
            for steps in range(4, 11):
                v = [width-1, height-1, 0, 0, 0, 0]
                v[dir_i + 2] = steps
                v = tuple(v)
                d = dist.get(v, inf)
                if d < answer:
                    answer = d
                    min_v = v

        path = graph.get_path(pred, min_v)
        print_path(path)

        print('Answer:', answer)
