import math
import re

"""
epic math time

t = button hold time
d(t) = distance
T = race time
v = velocity
R = record

d(t) > R
d(t) - R > 0

d(t) = v(T-t)
     = t(T-t)
     = -t^2 - Tt
since v = t

-t^2 - Tt - R > 0
[quadratic formula]
roots:
    t = T/2 + sqrt(T^2 - 4R)
    t = T/2 - sqrt(T^2 - 4R)
therefore d(t) > R for all t where
T/2 - sqrt(T^2 - 4R) < t < T/2 + sqrt(T^2 - 4R)
"""

def get_range(time, record):
    return math.sqrt(time**2 - 4*record)

def get_ways_to_win(time, record):
    r = get_range(time, record)
    lower = time/2 - r/2
    upper = time/2 + r/2

    lower = math.ceil(lower + 0.000001)
    upper = math.floor(upper - 0.000001)
    return upper - lower + 1

def parse_races(text):
    times, records = text.split('\n')

    times = times.removeprefix('Time:').strip()
    times = re.split(r'\s+', times)
    times = map(int, times)

    records = records.removeprefix('Distance:').strip()
    records = re.split(r'\s+', records)
    records = map(int, records)

    return list(zip(times, records))

if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        races = parse_races(file.read())
        answer = 1
        for time, record in races:
            ways = get_ways_to_win(time, record)
            answer *= ways
        print(answer)