def check_col(pattern, col):
    # returns true if the pattern is reflected vertically
    # along the line between columns col and col+1 (with 1 smudge)
    errors = 0
    for y in range(len(pattern)):
        width = min(col+1, len(pattern[0]) - col - 1)
        start = col-width+1
        end = col+width
        for i in range(width):
            if pattern[y][start+i] != pattern[y][end-i]:
                errors += 1
            if errors > 1:
                return False
    return errors == 1

def check_row(pattern, row):
    # returns true if the pattern is reflected horizontally
    # along the line between rows row and row+1 (with 1 smudge)
    errors = 0
    for x in range(len(pattern[0])):
        height = min(row+1, len(pattern) - row - 1)
        start = row-height+1
        end = row+height
        for i in range(height):
            if pattern[start+i][x] != pattern[end-i][x]:
                errors += 1
            if errors > 1:
                return False
    return errors == 1

def summarize(pattern):
    for row in range(len(pattern) - 1):
        if check_row(pattern, row):
            print('Reflects along row', row)
            return 100 * (row + 1)
    for col in range(len(pattern[0]) - 1):
        if check_col(pattern, col):
            print('Reflects along column', col)
            return col + 1
    raise RuntimeError('didnt find a reflection :(')

def parse_patterns(text):
    patterns = text.split('\n\n')
    for i in range(len(patterns)):
        patterns[i] = patterns[i].splitlines()
    return patterns

def print_pattern(pattern):
    for line in pattern:
        print(line)

if __name__ == '__main__':
    with open('input.txt') as file:
        answer = 0
        patterns = parse_patterns(file.read())
        for pattern in patterns:
            print_pattern(pattern)
            answer += summarize(pattern)
            print()
        print('Answer:', answer)
