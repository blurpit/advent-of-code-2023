import math
import re

"""
see part 1 for math
"""

def get_ways_to_win(time, record):
    r = math.sqrt(time**2 - 4*record)
    lower = time/2 - r/2
    upper = time/2 + r/2

    lower = math.ceil(lower + 0.000001)
    upper = math.floor(upper - 0.000001)
    return upper - lower + 1

def parse_race(text):
    times, records = text.split('\n')

    time = int(times.removeprefix('Time:').replace(' ', ''))
    record = int(records.removeprefix('Distance:').replace(' ', ''))
    return time, record

if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        time, record = parse_race(file.read())
        answer = get_ways_to_win(time, record)
        print(answer)