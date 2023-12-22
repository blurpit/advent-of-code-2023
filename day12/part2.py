import functools

@functools.cache # LITERAL MAGIC
def count_arrangements(row, record):
    # base case
    if not record:
        if '#' in row:
            # invalid: hashes that weren't counted in record
            return 0
        else:
            return 1
    if not row:
        if record:
            # invalid: leftover stuff in record
            return 0
        else:
            return 1


    arr = 0
    # If the first character is a dot, ignore it and continue.
    # If it's a hash, remove the block of #s from the record and continue.
    # If it's a question, do both of the above.

    if row[0] in '?.':
        arr += count_arrangements(row[1:], record)

    if row[0] in '?#':
        # In order to be valid, the next R characters need to be a single chunk
        # of hashes, where R is record[0]. We need to make sure that:
        # 1. row has at least R characters left
        # 2. there aren't any dots in the first R characters of row
        # 3. the chunk of hashes is exactly R long, i.e. that row[R] is not a hash.
        r = record[0]
        one = len(row) >= r
        two = '.' not in row[:r]
        three = r >= len(row) or row[r] != '#'
        if one and two and three:
            # Knock off the entire chunk of R hashes, removing it from the record too
            arr += count_arrangements(row[r+1:], record[1:])

    return arr

def parse_line(line):
    row, record = line.split(' ', 1)
    record = tuple(map(int, record.split(',')))
    return row, record

if __name__ == '__main__':
    with open('input.txt') as file:
        answer = 0
        for line in file.readlines():
            row, record = parse_line(line)
            # row = clean_row(row)
            row = '?'.join([row] * 5)
            record *= 5
            print(row)
            print(record)
            count = count_arrangements(row, record)
            answer += count
            print(count)
            print()
        print('Answer:', answer)
