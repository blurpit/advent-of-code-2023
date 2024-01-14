from collections import namedtuple

vec2 = namedtuple('vec2', ['x', 'y'])

class Ray:
    def __init__(self, line):
        pos, vel = line.split(' @ ', 1)
        pos = pos.strip().split(', ')
        vel = vel.strip().split(', ')

        px, py, pz = map(int, pos)
        vx, vy, vz = map(int, vel)

        self.pos = vec2(px, py)
        self.vel = vec2(vx, vy)

    def __str__(self):
        return (f'{self.pos.x}, {self.pos.y} @ '
                f'{self.vel.x}, {self.vel.y}')

def get_intersection(r1: Ray, r2: Ray):
    """ Returns the intersection point of two rays """
    # The rays intersect when p1 + v1*t1 = p2 + v2*t2
    # where t1 and t2 are scalar variables and p1, v1, p2, v2 and the pos/vel
    # of the two rays. Rearranging, we get
    # v1*t1 - v2*t2 = p2 - p1
    #
    # Expanding into a system of linear equations:
    # v1x * t1 - v2x * t2 = p2x - p1x
    # v1y * t1 - v2y * t2 = p2y - p1y
    #
    # And turning into a matrix equation At=b:
    # ⎡ v1x  -v2x ⎤ ⎡ t1 ⎤ = ⎡ p2x-p1x ⎤
    # ⎣ v1y  -v2y ⎦ ⎣ t2 ⎦   ⎣ p2y-p1y ⎦
    #
    # Using Cramer's rule to solve, we use these 2 matrices:
    # A1 = ⎡ p2x-p1x  -v2x ⎤   A2 = ⎡ v1x  p2x-p1x ⎤
    #      ⎣ p2y-p1y  -v2y ⎦        ⎣ v1y  p2y-p1y ⎦

    p1x, p1y = r1.pos
    v1x, v1y = r1.vel
    p2x, p2y = r2.pos
    v2x, v2y = r2.vel

    # determinants of A, A1, and A2
    detA = (v1x * -v2y) - (-v2x * v1y)
    detA1 = ((p2x-p1x) * -v2y) - (-v2x * (p2y-p1y))
    detA2 = (v1x * (p2y-p1y)) - ((p2x-p1x) * v1y)

    if detA == 0:
        return None

    t1 = detA1 / detA
    t2 = detA2 / detA

    # Check if paths cross in the past
    if t1 < 0 or t2 < 0:
        return None

    return vec2(
        p1x + v1x * t1,
        p1y + v1y * t1
    )

def inside_test_area(p: vec2, low, high):
    return low <= p.x <= high and low <= p.y <= high

if __name__ == '__main__':
    with open('input.txt') as file:
        stones = [Ray(line) for line in file.readlines()]
        # low, high = 7, 27
        low, high = 200000000000000, 400000000000000

        answer = 0
        for i in range(len(stones)):
            for j in range(i+1, len(stones)):
                a = stones[i]
                b = stones[j]
                # print('Hailstone A:', a)
                # print('Hailstone B:', b)
                p = get_intersection(a, b)
                if p:
                    if inside_test_area(p, low, high):
                        # print('intersection INSIDE at', p.x, p.y)
                        answer += 1
                #     else:
                #         print('intersection OUTSIDE at', p.x, p.y)
                # else:
                #     print('no intersection')
                # print()
        print('Answer:', answer)
