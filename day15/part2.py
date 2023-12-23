def HASH(s):
    val = 0
    for ch in s:
        code = ord(ch)
        val += code
        val *= 17
        val %= 256
    return val

def do_remove(label):
    box = HASH(label)
    boxes[box].pop(label, None)

def do_add(label, focal):
    box = HASH(label)
    boxes[box][label] = focal

def parse_step(step):
    if '=' in step:
        label, focal = step.split('=', 1)
        focal = int(focal)
        return label, focal, '='
    else:
        label = step.removesuffix('-')
        return label, 0, '-'

def focusing_power(box):
    power = 0
    for i, (label, focal) in enumerate(boxes[box].items(), 1):
        power += (1 + box) * i * focal
    return power

def print_boxes():
    for i, box in enumerate(boxes):
        if box:
            s = f'Box {i}:'
            for label, focal in box.items():
                s += f' [{label} {focal}]'
            print(s)
    print()

if __name__ == '__main__':
    with open('input.txt') as file:
        steps = file.readline().strip().split(',')
        answer = 0
        boxes = [{} for _ in range(256)]
        for step in steps:
            label, focal, action = parse_step(step)
            if action == '=':
                do_add(label, focal)
            else:
                do_remove(label)
            # print(f'After "{step}"')
            # print_boxes()

        answer = 0
        for box in range(len(boxes)):
            answer += focusing_power(box)
        print(answer)
