def tilt_north():
    for x in range(width):
        for y in range(1, height):
            if grid[y][x] == 'O':
                y2 = y-1
                while y2 >= 0 and grid[y2][x] == '.':
                    y2 -= 1
                grid[y][x] = '.'
                grid[y2+1][x] = 'O'

def tilt_south():
    for x in range(width):
        for y in range(height-1, -1, -1):
            if grid[y][x] == 'O':
                y2 = y+1
                while y2 < height and grid[y2][x] == '.':
                    y2 += 1
                grid[y][x] = '.'
                grid[y2-1][x] = 'O'

def tilt_west():
    for y in range(height):
        for x in range(1, width):
            if grid[y][x] == 'O':
                x2 = x-1
                while x2 >= 0 and grid[y][x2] == '.':
                    x2 -= 1
                grid[y][x] = '.'
                grid[y][x2+1] = 'O'

def tilt_east():
    for y in range(height):
        for x in range(width-1, -1, -1):
            if grid[y][x] == 'O':
                x2 = x+1
                while x2 < width and grid[y][x2] == '.':
                    x2 += 1
                grid[y][x] = '.'
                grid[y][x2-1] = 'O'

def cycle():
    tilt_north()
    tilt_west()
    tilt_south()
    tilt_east()

def run_cycles(n):
    while True:
        g = grid_to_str()
        if g in cache:
            i = cache.index(g)
            print('Cycle', len(cache), 'matched cycle', i)
            loop_length = len(cache) - i
            cycles_left = n - i
            i = i + cycles_left % loop_length
            print('Cycle', n, 'matches cycle', i)
            return parse_grid(cache[i])
        cache.append(g)
        cycle()
        print('Cycle', len(cache)-1)

def grid_to_str():
    return '\n'.join(''.join(row) for row in grid)

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

def parse_grid(text):
    return [list(line) for line in text.splitlines()]

if __name__ == '__main__':
    with open('input.txt') as file:
        grid = parse_grid(file.read())
        width = len(grid[0])
        height = len(grid)
        cache = []
        grid = run_cycles(1000000000)
        print('Answer:', get_load())