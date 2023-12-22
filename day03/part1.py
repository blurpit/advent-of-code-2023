def check_symbols(grid, x, y):
    """ Returns true if there is a symbol at (x, y-1), (x, y), or (x, y+1) """
    width = len(grid)
    height = len(grid[0])

    for dy in (-1, 0, 1):
        y2 = y + dy
        if 0 <= x < width and 0 <= y2 < height: # check grid bounds
            ch = grid[y2][x]
            if ch != '.' and not ch.isdigit():
                return True
    return False

def get_part_number(grid, x, y):
    """ Given an (x, y) position that is the start (leftmost digit) of a number,
        return the number *as a string* and True/False if it was adjacent to a
        symbol. """
    width = len(grid[0])
    adjacent = False
    num = ''

    # . . . . . .
    # . 1 2 3 4 .
    # . . . . . .

    # Check left edge
    if check_symbols(grid, x - 1, y):
        adjacent = True

    # Check middle digits
    while x < width and grid[y][x].isdigit():
        if not adjacent and check_symbols(grid, x, y):
            adjacent = True
        num += grid[y][x]
        x += 1

    # Check right edge
    if not adjacent and check_symbols(grid, x, y):
        adjacent = True

    return num, adjacent

def get_part_number_sum(grid):
    total = 0
    width = len(grid)
    height = len(grid[0])

    x = 0
    for y in range(height):
        while x < width:
            if grid[y][x].isdigit():
                num, adjacent = get_part_number(grid, x, y)
                if adjacent:
                    total += int(num)
                x += len(num)
            else:
                x += 1
        x = 0

    return total

if __name__ == '__main__':
    grid = []
    with open('input.txt', 'r') as file:
        for line in file.readlines():
            grid.append(list(line.strip()))
    answer = get_part_number_sum(grid)
    print(answer)
