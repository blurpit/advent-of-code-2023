"""
Had to cheat a bit for this one.
Critical info obtained from internet people who are smarter than me:
    The number of reachable plots grows according to some quadratic function
    f(x) = ax^2 + bx + c
    where x is the number of steps we're taking.

This means we can sample the function for small numbers of steps (using BFS)
and use 3 such sample points to calculate a, b, and c, then plug in our desired
huge number of steps to get the final answer.

f(x) seems to only approximate the correct answer unless x is an exact multiple
of the size of the tile. Probably because of the repetitive nature of adding
tiles, that growing the diamond by 1 tile fits a parabola exactly. The real
input starts in the center of a tile, and taking 26,501,365 steps conveniently
lands right on the edge of a tile, 202300 tiles out. So f(26501365) will indeed
be the correct answer.
"""
import numpy as np

from util import Graph, Queue

NORTH = (0, -1)
EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)
DIRECTIONS = [EAST, SOUTH, WEST, NORTH]


def find_start():
    for y in range(size):
        for x in range(size):
            if tile[y][x] == 'S':
                return x, y

def convert_pos(x, y):
    """ converts (x, y) as steps away from S to (x, y) positions relative to
        the top-left corner of a single tile. """
    return (x + sx) % size, (-y + sy) % size

def get_at(x, y):
    x, y = convert_pos(x, y)
    return tile[y][x]

def set_at(x, y, ch):
    x, y = convert_pos(x, y)
    tile[y][x] = ch

class TileGraph(Graph):
    def __init__(self, steps):
        super().__init__()
        self.steps = steps

    def get_neighbors(self, u, d=0):
        x, y = u
        for dx, dy in DIRECTIONS:
            # manhattan_dist = abs(x + dx) + abs(y + dy)
            if d <= self.steps and get_at(x + dx, y + dy) != '#':
                yield (x + dx, y + dy), 1

    def count_reachable(self):
        count = 0

        def mark(v, d):
            nonlocal count
            x, y = v
            # The space is reachable if the distance from the origin has the
            # same parity as the number of steps we're taking.
            if d % 2 == self.steps % 2:
                count += 1
                # set_at(x, y, 'O')

        # Run BFS from the origin
        self.wfs((0, 0), Queue(), mark)
        return count

def sample_points(steps_samples):
    samples = []
    for steps in steps_samples:
        samples.append(TileGraph(steps).count_reachable())
    return samples

def calc_coefficients(x_samples, y_samples):
    A = [[x**2, x, 1] for x in x_samples]
    a, b, c = np.linalg.solve(A, y_samples)
    return a, b, c

def calc_reachable(a, b, c, x):
    return a*x*x + b*x + c

def print_tile(tile):
    for row in tile:
        print(''.join(row))
    print()


if __name__ == '__main__':
    with open('input.txt') as file:
        tile = [list(line.strip()) for line in file.readlines()]
        size = len(tile)
        sx, sy = find_start()

        steps = [65, 196, 327]
        samples = sample_points(steps)
        print(steps)
        print(samples)
        a, b, c = calc_coefficients(steps, samples)
        print(a, b, c)

        print()
        print(calc_reachable(a, b, c, 26501365))
