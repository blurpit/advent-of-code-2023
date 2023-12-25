NORTH = (0, -1)
EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)
directions = [EAST, SOUTH, WEST, NORTH]

def plan_to_points(plan):
    x, y = 0, 0
    for (dx, dy), steps in plan:
        x += dx * steps
        y += dy * steps
        yield x, y

def perimeter(plan):
    return sum(steps for _, steps in plan)

def parse_step(line):
    _, _, color = line.strip().split(' ')
    color = color.removeprefix('(#').removesuffix(')')
    d = int(color[-1])
    steps = int(color[:-1], 16)
    return directions[d], steps

def cross_prod(x1, y1, x2, y2):
    return x1 * y2 - y1 * x2

def area(points):
    total = 0
    for i in range(len(points)):
        (x1, y1) = points[i]
        (x2, y2) = points[(i + 1) % len(points)]
        total += cross_prod(x1, y1, x2, y2)
    return abs(total) / 2

if __name__ == '__main__':
    with open('input.txt') as file:
        plan = [parse_step(line) for line in file.readlines()]
        points = list(plan_to_points(plan))
        # print(points)

        P = perimeter(plan)
        A = area(points)
        print(f'A={A} P={P}')

        # https://en.wikipedia.org/wiki/Pick%27s_theorem
        # A = i + b/2 - 1
        # where i = number of interior lattice points and b is boundary lattice points.
        # Since all our edges here are axis-aligned, b is simply the perimeter P.
        # Therefore answer = i + P
        #   = A - P/2 + 1 + P
        #   = A + P/2 + 1
        answer = A + 1 + P/2
        print('Answer:', round(answer))
