NORTH = (0, -1)
EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)

# Maps a starting direction and a character to the new direction
# after following that pipe.
transitions = {
    NORTH: {
        '|': NORTH,
        '7': WEST,
        'F': EAST
    },
    EAST: {
        '-': EAST,
        '7': SOUTH,
        'J': NORTH
    },
    SOUTH: {
        '|': SOUTH,
        'L': EAST,
        'J': WEST
    },
    WEST: {
        '-': WEST,
        'L': NORTH,
        'F': SOUTH
    }
}

# Positions to the RIGHT of a pipe given the direction facing
# after moving along that pipe.
RIGHT = {
    '|': {
        # .|R
        NORTH: [(1, 0)],
        # R|.
        SOUTH: [(-1, 0)],
    },
    '-': {
        # .
        # -
        # R
        EAST: [(0, 1)],
        # R
        # -
        # .
        WEST: [(0, -1)],
    },
    'L': {
        # RL
        # RR
        EAST: [(-1, 0), (-1, 1), (0, 1)],
        # .L
        # ..
        NORTH: [],
    },
    'J': {
        # J.
        # ..
        WEST: [],
        # JR
        # RR
        NORTH: [(1, 0), (1, 1), (0, 1)],
    },
    '7': {
        # RR
        # 7R
        WEST: [(0, -1), (1, -1), (1, 0)],
        # ..
        # 7.
        SOUTH: [],
    },
    'F': {
        # ..
        # .F
        EAST: [],
        # RR
        # RF
        SOUTH: [(-1, 0), (-1, -1), (0, -1)],
    },
}


def get_next(pos, direction):
    x = pos[0] + direction[0]
    y = pos[1] + direction[1]
    if 0 <= x < width and 0 <= y < height:
        ch = grid[y][x]
        next_dir = transitions[direction].get(ch)
        if next_dir:
            return (x, y), next_dir
    return (0, 0), None

def find_start():
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 'S':
                return x, y

def march_loop(start, paint):
    x, y = start
    grid2[y][x] = '*'
    current_dir = None
    length = 0

    # find start direction
    for direction in transitions:
        (x, y), current_dir = get_next(start, direction)
        if current_dir:
            break

    while current_dir is not None:
        grid2[y][x] = '*'
        if paint:
            paint_bucket(x, y, current_dir, 'R')
        (x, y), current_dir = get_next((x, y), current_dir)
        length += 1

    return length + 1

def paint_bucket(sx, sy, direction, ch):
    stack = []
    for (dx, dy) in RIGHT[grid[sy][sx]][direction]:
        stack.append((sx + dx, sy + dy))

    while stack:
        x, y = stack.pop()
        if 0 <= x < width and 0 <= y < height and grid2[y][x] == '.':
            grid2[y][x] = ch
            for dx, dy in transitions:
                stack.append((x + dx, y + dy))

def count(ch):
    num = 0
    for y in range(height):
        for x in range(width):
            if grid2[y][x] == ch:
                num += 1
    return num

def print_grid(grid):
    for line in grid:
        print(''.join(line))
    print()

if __name__ == '__main__':
    with open('input.txt') as file:
        grid = [list(l.strip()) for l in file.readlines()]
        width = len(grid[0])
        height = len(grid)
        grid2 = [['.' for x in range(width)] for y in range(height)]
        start = find_start()

        # first pass marks characters along the loop with *
        march_loop(start, False)
        # 2nd pass paint-buckets all the characters on one side of the loop
        march_loop(start, True)

        print_grid(grid)
        print_grid(grid2)

        # One of these is the answer. Can't be bothered to figure out which is
        # inside the loop and which is outside.
        lefts = count('.')
        rights = count('R')
        print(lefts, rights)
