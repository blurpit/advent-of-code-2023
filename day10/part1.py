NORTH = (0, -1)
EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)

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

def get_next(grid, pos, direction):
    width = len(grid[0])
    height = len(grid)
    x = pos[0] + direction[0]
    y = pos[1] + direction[1]
    if 0 <= x < width and 0 <= y < height:
        ch = grid[y][x]
        next_dir = transitions[direction].get(ch)
        if next_dir:
            return (x, y), next_dir
    return None, None

def find_start(grid):
    width = len(grid[0])
    height = len(grid)
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 'S':
                return x, y

def march_loop(grid, start):
    pos = start
    current_dir = None
    length = 0

    # find start direction
    for direction in transitions:
        pos, current_dir = get_next(grid, start, direction)
        if pos:
            break

    while pos is not None:
        pos, current_dir = get_next(grid, pos, current_dir)
        length += 1

    return length + 1

if __name__ == '__main__':
    with open('input.txt') as file:
        grid = [l.strip() for l in file.readlines()]
        start = find_start(grid)
        length = march_loop(grid, start)
        print(length // 2)