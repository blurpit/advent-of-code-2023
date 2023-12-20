def parse_line(line):
    return [int(x.strip()) for x in line.split(' ')]

def predict_first(history):
    diffs = [history]
    while any(x != 0 for x in diffs[-1]):
        diffs.append(get_diff(diffs[-1]))

    value = 0
    for diff in reversed(diffs):
        value = diff[0] - value
    return value

def get_diff(history):
    diff = []
    for i in range(1, len(history)):
        diff.append(history[i] - history[i-1])
    return diff

if __name__ == '__main__':
    answer = 0
    with open('input.txt', 'r') as file:
        for line in file.readlines():
            value = predict_first(parse_line(line))
            answer += value
    print(answer)