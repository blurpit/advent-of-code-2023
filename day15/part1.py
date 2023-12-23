def HASH(s):
    val = 0
    for ch in s:
        code = ord(ch)
        val += code
        val *= 17
        val %= 256
    return val

if __name__ == '__main__':
    with open('input.txt') as file:
        steps = file.readline().strip().split(',')
        answer = 0
        for step in steps:
            answer += HASH(step)
        print(answer)
