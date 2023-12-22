def get_number_at(grid, x, y, dupe_positions):
    """ Given an (x, y) that contains a digit, returns the number that that
        digit is a part of """
    width = len(grid[0])
    x0 = x
    num = ''

    # Left side
    while x >= 0 and grid[y][x].isdigit():
        num = grid[y][x] + num
        x -= 1

    # Right side
    x = x0 + 1
    while x < width and grid[y][x].isdigit():
        num = num + grid[y][x]
        dupe_positions.add((x, y))
        x += 1

    return int(num)

def get_adjacent_numbers(grid, x, y):
    """ Returns a list of numbers adjacent to (x, y) """
    height = len(grid)
    width = len(grid[0])
    numbers = []
    # Some numbers are touching the gear at multiple positions. Put those
    # positions into a set so we can skip over them.
    dupe_positions = set()

    for dy in range(-1, 2):
        for dx in range(-1, 2):
            x2 = x + dx
            y2 = y + dy
            if (0 <= x2 < width and 0 <= y < height # check bounds
                    and (x2, y2) not in dupe_positions
                    and grid[y2][x2].isdigit()):
                num = get_number_at(grid, x2, y2, dupe_positions)
                numbers.append(num)

    return numbers

def get_gear_ratio(grid, x, y):
    """ Returns the gear ratio of a * symbol positioned at (x, y) if it
        is a gear (has exactly 2 adjacent numbers), and returns 0 otherwise."""
    numbers = get_adjacent_numbers(grid, x, y)
    if len(numbers) == 2:
        return numbers[0] * numbers[1]
    return 0

if __name__ == '__main__':
    grid = []
    with open('input.txt', 'r') as file:
        for line in file.readlines():
            grid.append(list(line.strip()))

    answer = 0
    height = len(grid)
    width = len(grid[0])
    for y in range(height):
        for x in range(width):
            if grid[y][x] == '*':
                answer += get_gear_ratio(grid, x, y)
    print(answer)
