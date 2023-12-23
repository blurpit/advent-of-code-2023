NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (-1, 0)

def shine_beam(sx, sy, direction):
    # shine in a straight line
    x, y = sx, sy
    dx, dy = direction
    while 0 <= x < width and 0 <= y < height and grid[y][x] == '.':
        if is_energized(x, y, direction):
            return

        energize(x, y, direction)
        x += dx
        y += dy

    # out of bounds
    if not 0 <= x < width or not 0 <= y < height:
        return

    # set energized
    energize(x, y, direction)

    # horizontal splitter
    if grid[y][x] == '-':
        if direction == EAST or direction == WEST:
            # beam passes through
            shine_beam(x + dx, y + dy, direction)
        else:
            # split the beam into east/west
            dx, dy = EAST
            shine_beam(x + dx, y + dy, EAST)
            dx, dy = WEST
            shine_beam(x + dx, y + dy, WEST)

    # vertical splitter
    if grid[y][x] == '|':
        if direction == NORTH or direction == SOUTH:
            # beam passes through
            shine_beam(x + dx, y + dy, direction)
        else:
            # split the beam into north/south
            dx, dy = NORTH
            shine_beam(x + dx, y + dy, NORTH)
            dx, dy = SOUTH
            shine_beam(x + dx, y + dy, SOUTH)

    # / mirror
    if grid[y][x] == '/':
        if direction == NORTH:
            new_dir = EAST
        elif direction == SOUTH:
            new_dir = WEST
        elif direction == EAST:
            new_dir = NORTH
        else: # WEST
            new_dir = SOUTH
        dx, dy = new_dir
        shine_beam(x + dx, y + dy, new_dir)

    # \ mirror
    if grid[y][x]  == '\\':
        if direction == NORTH:
            new_dir = WEST
        elif direction == SOUTH:
            new_dir = EAST
        elif direction == EAST:
            new_dir = SOUTH
        else: # WEST
            new_dir = NORTH
        dx, dy = new_dir
        shine_beam(x + dx, y + dy, new_dir)

def energize(x, y, direction):
    if direction == NORTH:
        energized[y][x] |= 0b0001
    elif direction == SOUTH:
        energized[y][x] |= 0b0010
    elif direction == EAST:
        energized[y][x] |= 0b0100
    elif direction == WEST:
        energized[y][x] |= 0b1000

def is_energized(x, y, direction):
    if direction == NORTH:
        return energized[y][x] & 0b0001 > 0
    elif direction == SOUTH:
        return energized[y][x] & 0b0010 > 0
    elif direction == EAST:
        return energized[y][x] & 0b0100 > 0
    elif direction == WEST:
        return energized[y][x] & 0b1000 > 0

def count_energized():
    count = 0
    for y in range(height):
        for x in range(width):
            if energized[y][x]:
                count += 1
    return count

def print_grid():
    for row in grid:
        print(row)
    print()

def print_energized_grid():
    for row in energized:
        for x in row:
            print('#' if x else '.', end='')
        print()
    print()

if __name__ == '__main__':
    with open('input.txt') as file:
        grid = [line.strip() for line in file.readlines()]
        width = len(grid[0])
        height = len(grid)
        energized = [[0 for x in range(width)] for y in range(height)]
        print_grid()

        shine_beam(0, 0, EAST)
        print_energized_grid()

        print(count_energized())
