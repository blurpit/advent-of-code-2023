NUMBERS = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'zero': 0,
}
NUMBERS_REV = {word[::-1]: n for word, n in NUMBERS.items()}

def get_calibration_num(line):
    num = get_first_digit(line, NUMBERS) # First digit
    num *= 10
    num += get_first_digit(line[::-1], NUMBERS_REV) # Last digit
    return num

def get_first_digit(line, numbers):
    for i, c in enumerate(line):
        # Check for digit
        if c.isdigit():
            return int(c)

        # Check for number words
        for word, num in numbers.items():
            match = True
            for j in range(len(word)):
                if i+j >= len(line) or word[j] != line[i+j]:
                    match = False
                    break
            if match:
                return num

if __name__ == '__main__':
    answer = 0
    with open('input.txt', 'r') as file:
        for line in file.readlines():
            answer += get_calibration_num(line)
    print('Answer:', answer)
