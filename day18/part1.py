from math import inf

NORTH = (0, -1)
EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)
directions = {
    'U': NORTH,
    'D': SOUTH,
    'R': EAST,
    'L': WEST,
}

def calc_size(plan):
    min_x = inf
    max_x = -inf
    min_y = inf
    max_y = -inf
    x, y = 0, 0
    for d, steps in plan:
        dx, dy = directions[d]
        x += dx * steps
        y += dy * steps
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    width = max_x - min_x + 1
    height = max_y - min_y + 1
    return width, height, (abs(min_x), abs(min_y))

def march_plan(plan):
    x, y = 0, 0
    grid[y + off_y][x + off_x] = '#'
    for d, steps in plan:
        dx, dy = directions[d]
        for s in range(steps):
            x += dx
            y += dy
            grid[y + off_y][x + off_x] = '#'

def first_hash():
    for y in range(height):
        for x in range(width):
            if grid[y][x] == '#':
                return x, y

def fill():
    # (x, y) is guaranteed to be a top-left corner.
    # (x+1, y+1) is therefore inside the shape, so we can paint bucket fill it.
    x, y = first_hash()
    stack = [(x+1, y+1)]
    while stack:
        x, y = stack.pop()
        if grid[y][x] == '.':
            grid[y][x] = '#'
            for dx, dy in directions.values():
                if 0 <= x + dx < width and 0 <= y + dy < height:
                    stack.append((x + dx, y + dy))

def count_hash():
    count = 0
    for y in range(height):
        for x in range(width):
            if grid[y][x] == '#':
                count += 1
    return count

def parse_step(line):
    direction, num, _ = line.strip().split(' ')
    return direction, int(num)

def print_grid():
    for row in grid:
        print(''.join(row))
    print()

if __name__ == '__main__':
    with open('input.txt') as file:
        plan = [parse_step(line) for line in file.readlines()]
        print(plan)

        width, height, (off_x, off_y) = calc_size(plan)
        print(width, height, off_x, off_y)

        grid = [['.'] * width for _ in range(height)]
        march_plan(plan)
        fill()
        print_grid()

        print('Answer:', count_hash())
