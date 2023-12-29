NORTH = (0, -1)
EAST = (1, 0)
SOUTH = (0, 1)
WEST = (-1, 0)
directions = [EAST, SOUTH, WEST, NORTH]

def copy_grid(grid):
    return [
        row.copy()
        for row in grid
    ]

def find_start(grid):
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 'S':
                return x, y

def expand(grid):
    output = copy_grid(blank_grid)
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 'O':
                for dx, dy in directions:
                    if (0 <= x + dx < width
                            and 0 <= y + dy < height
                            and grid[y + dy][x + dx] == '.'):
                        output[y + dy][x + dx] = 'O'
    return output

def count_os(grid):
    count = 0
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 'O':
                count += 1
    return count

def print_grid(grid):
    for row in grid:
        print(''.join(row))
    print()

if __name__ == '__main__':
    with open('input.txt') as file:
        blank_grid = [list(line.strip()) for line in file.readlines()]
        width = len(blank_grid[0])
        height = len(blank_grid)

        sx, sy = find_start(blank_grid)
        g = copy_grid(blank_grid)
        blank_grid[sy][sx] = '.'
        g[sy][sx] = 'O'

        for i in range(64):
            g = expand(g)

        print_grid(g)
        print(count_os(g))
