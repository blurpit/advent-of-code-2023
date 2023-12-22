def tilt_north():
    for x in range(width):
        for y in range(1, height):
            if grid[y][x] == 'O':
                y2 = y-1
                while y2 >= 0 and grid[y2][x] == '.':
                    y2 -= 1
                grid[y][x] = '.'
                grid[y2+1][x] = 'O'

def get_load():
    load = 0
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 'O':
                load += (height - y)
    return load

def print_grid():
    for row in grid:
        print(''.join(row))
    print()

if __name__ == '__main__':
    with open('input.txt') as file:
        grid = [list(line) for line in file.read().splitlines()]
        width = len(grid[0])
        height = len(grid)
        print_grid()
        tilt_north()
        print_grid()
        print(get_load())
