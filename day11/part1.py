def expand():
    # expand rows
    for y in range(len(grid)-1, -1, -1):
        row = grid[y]
        if all(c == '.' for c in row):
            grid.insert(y, row.copy())

    # expand columns
    for x in range(len(grid[0])-1, -1, -1):
        col = [grid[y][x] for y in range(len(grid))]
        if all(c == '.' for c in col):
            for row in grid:
                row.insert(x, '.')

def find_galaxies():
    galaxies = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '#':
                galaxies.append((x, y))
    return galaxies

def manhattan_dist(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

def print_grid():
    for line in grid:
        print(''.join(line))
    print()

if __name__ == '__main__':
    with open('input.txt') as file:
        grid = [list(l.strip()) for l in file.readlines()]
        expand()

        galaxies = find_galaxies()
        answer = 0
        for i in range(len(galaxies)):
            for j in range(i+1, len(galaxies)):
                answer += manhattan_dist(galaxies[i], galaxies[j])
        print(answer)