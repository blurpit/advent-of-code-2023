def find_galaxies():
    galaxies = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '#':
                galaxies.append((x, y))
    return galaxies

def find_empty_rows_cols():
    # cache which rows & cols are empty cause checking every time
    # is way too slow
    rows = []
    cols = []

    for y in range(height):
        if all(grid[y][x] == '.' for x in range(width)):
            rows.append(True)
        else:
            rows.append(False)

    for x in range(width):
        if all(grid[y][x] == '.' for y in range(height)):
            cols.append(True)
        else:
            cols.append(False)

    return rows, cols

def is_col_empty(x):
    return empty_cols[x]

def is_row_empty(y):
    return empty_rows[y]

def distance(p1, p2, mul):
    dist = 0
    x1 = min(p1[0], p2[0])
    x2 = max(p1[0], p2[0])
    y1 = min(p1[1], p2[1])
    y2 = max(p1[1], p2[1])

    # horizontal
    for x in range(x1, x2):
        if is_col_empty(x):
            dist += mul
        else:
            dist += 1

    # vertical
    for y in range(y1, y2):
        if is_row_empty(y):
            dist += mul
        else:
            dist += 1

    return dist

if __name__ == '__main__':
    with open('input.txt') as file:
        grid = [list(l.strip()) for l in file.readlines()]
        width = len(grid[0])
        height = len(grid)

        galaxies = find_galaxies()
        empty_rows, empty_cols = find_empty_rows_cols()

        answer = 0
        for i in range(len(galaxies)):
            for j in range(i+1, len(galaxies)):
                answer += distance(galaxies[i], galaxies[j], 1000000)
        print(answer)