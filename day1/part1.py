def get_calibration_num(line: str) -> int:
    num = 0
    # First digit
    for c in line:
        if c.isdigit():
            num += int(c)
            break

    # Last digit
    num *= 10
    for c in reversed(line):
        if c.isdigit():
            num += int(c)
            break
    return num

if __name__ == '__main__':
    answer = 0
    with open('input1.txt', 'r') as file:
        for line in file.readlines():
            answer += get_calibration_num(line)
    print('Answer:', answer)
