from collections import namedtuple
from copy import deepcopy
from typing import List

"""
Our rock hits the first hailstone at t0, giving the following equations:
    p0x + v0x * t0 = pRx + vRx * t0
    p0y + v0y * t0 = pRy + vRy * t0
    p0z + v0z * t0 = pRz + vRz * t0
where p0, v0 is the hailstone ray and pR, vR is the rock ray (pos, vel).

Solving for t0:
    t0 = (pRx - p0x) / (v0x - vRx)
    t0 = (pRy - p0y) / (v0y - vRy)
    t0 = (pRz - p0z) / (v0z - vRz)

Setting these equal to each other to eliminate t0 gives this system of 
equations:
    (pRx - p0x) / (v0x - vRx) = (pRy - p0y) / (v0y - vRy)
    (pRx - p0x) / (v0x - vRx) = (pRz - p0z) / (v0z - vRz)

Multiply both sides by both denominators to get rid of the division:
    (pRx - p0x) * (v0y - vRy) = (pRy - p0y) * (v0x - vRx)
    (pRx - p0x) * (v0z - vRz) = (pRz - p0z) * (v0x - vRx)

Expand:
    pRx*v0y - pRx*vRy - p0x*v0y + p0x*vRy = pRy*v0x - pRy*vRx - p0y*v0x + p0y*vRx
    pRx*v0z - pRx*vRz - p0x*v0z + p0x*vRz = pRz*v0x - pRz*vRx - p0z*v0x + p0z*vRx

We have 6 unknowns here: pRx, pRy, pRz, vRx, vRy, and vRz. We want a system of
equations that looks like linear:
a*pRx + b*pRy + c*pRz + d*vRx + e*vRy + f*vRz = g

Let's put all terms with an unknown on the left and knowns on the right, reorder 
each term so unknowns are on the right side, and reorder the terms so the 
unknowns are in order (px, py, pz, vx, vy, vz).
    v0y*pRx - v0x*pRy - p0y*vRx + p0x*vRy + pRy*vRx - pRx*vRy = p0x*v0y - p0y*v0x
    v0z*pRx - v0x*pRz - p0z*vRx + p0x*vRz + pRz*vRx - pRx*vRz = p0x*v0z - p0z*v0x

Let's now generalize these equations. The rock hits hailstone 0 at t0, but this
is true for any hailstone. Hailstone N hits the rock at tN. So, we can 
generalize the equations by simply replacing hailstone 0 with N:
    vNy*pRx - vNx*pRy - pNy*vRx + pNx*vRy + pRy*vRx - pRx*vRy = pNx*vNy - pNy*vNx
    vNz*pRx - vNx*pRz - pNz*vRx + pNx*vRz + pRz*vRx - pRx*vRz = pNx*vNz - pNz*vNx
    
We unfortunately have some pesky terms where we're multiplying two unknowns 
together, so to get rid of those let's subtract the generalized equations from 
the equations using hailstone 0, since those terms are identical in both 
equations:
    v0y*pRx - v0x*pRy - p0y*vRx + p0x*vRy + pRy*vRx - pRx*vRy - (vNy*pRx - vNx*pRy - pNy*vRx + pNx*vRy + pRy*vRx - pRx*vRy) = p0x*v0y - p0y*v0x - (pNx*vNy - pNy*vNx)
    v0z*pRx - v0x*pRz - p0z*vRx + p0x*vRz + pRz*vRx - pRx*vRz - (vNz*pRx - vNx*pRz - pNz*vRx + pNx*vRz + pRz*vRx - pRx*vRz) = p0x*v0z - p0z*v0x - (pNx*vNz - pNz*vNx)

Swapping signs to get rid of the parentheses:
    v0y*pRx - v0x*pRy - p0y*vRx + p0x*vRy + pRy*vRx - pRx*vRy - vNy*pRx + vNx*pRy + pNy*vRx - pNx*vRy - pRy*vRx + pRx*vRy = p0x*v0y - p0y*v0x - pNx*vNy + pNy*vNx
    v0z*pRx - v0x*pRz - p0z*vRx + p0x*vRz + pRz*vRx - pRx*vRz - vNz*pRx + vNx*pRz + pNz*vRx - pNx*vRz - pRz*vRx + pRx*vRz = p0x*v0z - p0z*v0x - pNx*vNz + pNz*vNx

Getting rid of the terms that we cancelled out:
    v0y*pRx - v0x*pRy - p0y*vRx + p0x*vRy - vNy*pRx + vNx*pRy + pNy*vRx - pNx*vRy = p0x*v0y - p0y*v0x - pNx*vNy + pNy*vNx
    v0z*pRx - v0x*pRz - p0z*vRx + p0x*vRz - vNz*pRx + vNx*pRz + pNz*vRx - pNx*vRz = p0x*v0z - p0z*v0x - pNx*vNz + pNz*vNx

Reordering terms again:
    v0y*pRx - vNy*pRx + vNx*pRy  - v0x*pRy + pNy*vRx - p0y*vRx + p0x*vRy - pNx*vRy = p0x*v0y - p0y*v0x - pNx*vNy + pNy*vNx
    v0z*pRx - vNz*pRx + vNx*pRz  - v0x*pRz + pNz*vRx - p0z*vRx + p0x*vRz - pNx*vRz = p0x*v0z - p0z*v0x - pNx*vNz + pNz*vNx

Factoring each unknown:
    (v0y - vNy)pRx + (vNx - v0x)pRy + (pNy - p0y)vRx + (p0x - pNx)vRy = p0x*v0y - p0y*v0x - pNx*vNy + pNy*vNx
    (v0z - vNz)pRx + (vNx - v0x)pRz + (pNz - p0z)vRx + (p0x - pNx)vRz = p0x*v0z - p0z*v0x - pNx*vNz + pNz*vNx

Finally, adding in the missing coefficients:
    (v0y - vNy)pRx + (vNx - v0x)pRy + (    0    )pRz + (pNy - p0y)vRx + (p0x - pNx)vRy + (    0    )vRz = p0x*v0y - p0y*v0x - pNx*vNy + pNy*vNx
    (v0z - vNz)pRx + (    0    )pRy + (vNx - v0x)pRz + (pNz - p0z)vRx + (    0    )vRy + (p0x - pNx)vRz = p0x*v0z - p0z*v0x - pNx*vNz + pNz*vNx


These are now a linear system of equations! We have 6 unknowns, which means we 
need 6 equations. Since we generalized the equations to use any hailstone N,
we can simply substitute any 3 hailstones (except 0) for N to get our 6 
equations:
    (v0y - v1y)pRx + (v1x - v0x)pRy + (    0    )pRz + (p1y - p0y)vRx + (p0x - p1x)vRy + (    0    )vRz = p0x*v0y - p0y*v0x - p1x*v1y + p1y*v1x
    (v0z - v1z)pRx + (    0    )pRy + (v1x - v0x)pRz + (p1z - p0z)vRx + (    0    )vRy + (p0x - p1x)vRz = p0x*v0z - p0z*v0x - p1x*v1z + p1z*v1x
    (v0y - v2y)pRx + (v2x - v0x)pRy + (    0    )pRz + (p2y - p0y)vRx + (p0x - p2x)vRy + (    0    )vRz = p0x*v0y - p0y*v0x - p2x*v2y + p2y*v2x
    (v0z - v2z)pRx + (    0    )pRy + (v2x - v0x)pRz + (p2z - p0z)vRx + (    0    )vRy + (p0x - p2x)vRz = p0x*v0z - p0z*v0x - p2x*v2z + p2z*v2x
    (v0y - v3y)pRx + (v3x - v0x)pRy + (    0    )pRz + (p3y - p0y)vRx + (p0x - p3x)vRy + (    0    )vRz = p0x*v0y - p0y*v0x - p3x*v3y + p3y*v3x
    (v0z - v3z)pRx + (    0    )pRy + (v3x - v0x)pRz + (p3z - p0z)vRx + (    0    )vRy + (p0x - p3x)vRz = p0x*v0z - p0z*v0x - p3x*v3z + p3z*v3x

Now we can solve this as a normal system of linear equations using the matrix
equation Av = b:
    ⎡ v0y-v1y   v1x-v0x      0      p1y-p0y   p0x-p1x      0    ⎤ ⎡ pRx ⎤   ⎡ p0x*v0y - p0y*v0x - p1x*v1y + p1y*v1x ⎤
    ⎢ v0z-v1z      0      v1x-v0x   p1z-p0z      0      p0x-p1x ⎢ ⎢ pRy ⎢   ⎢ p0x*v0z - p0z*v0x - p1x*v1z + p1z*v1x ⎢
    ⎢ v0y-v2y   v2x-v0x      0      p2y-p0y   p0x-p2x      0    ⎢ ⎢ pRz ⎢ = ⎢ p0x*v0y - p0y*v0x - p2x*v2y + p2y*v2x ⎢
    ⎢ v0z-v2z      0      v2x-v0x   p2z-p0z      0      p0x-p2x ⎢ ⎢ vRx ⎢   ⎢ p0x*v0z - p0z*v0x - p2x*v2z + p2z*v2x ⎢
    ⎢ v0y-v3y   v3x-v0x      0      p3y-p0y   p0x-p3x      0    ⎢ ⎢ vRy ⎢   ⎢ p0x*v0y - p0y*v0x - p3x*v3y + p3y*v3x ⎢
    ⎣ v0z-v3z      0      v3x-v0x   p3z-p0z      0      p0x-p3x ⎦ ⎣ vRz ⎦   ⎣ p0x*v0z - p0z*v0x - p3x*v3z + p3z*v3x ⎦
"""

vec3 = namedtuple('vec2', ['x', 'y', 'z'])

class Ray:
    def __init__(self, pos: vec3, vel: vec3):
        self.pos = pos
        self.vel = vel

    def __str__(self):
        return (f'{self.pos.x}, {self.pos.y}, {self.pos.z} @ '
                f'{self.vel.x}, {self.vel.y}, {self.vel.z}')

def get_rock(stones: List[Ray]):
    """ Returns a Ray that intersects all other given rays """
    # Extract known variables
    p0x, p0y, p0z = stones[0].pos
    v0x, v0y, v0z = stones[0].vel
    p1x, p1y, p1z = stones[1].pos
    v1x, v1y, v1z = stones[1].vel
    p2x, p2y, p2z = stones[2].pos
    v2x, v2y, v2z = stones[2].vel
    p3x, p3y, p3z = stones[3].pos
    v3x, v3y, v3z = stones[3].vel

    A = [
        [ v0y-v1y,   v1x-v0x,      0,      p1y-p0y,   p0x-p1x,      0,    ],
        [ v0z-v1z,      0,      v1x-v0x,   p1z-p0z,      0,      p0x-p1x, ],
        [ v0y-v2y,   v2x-v0x,      0,      p2y-p0y,   p0x-p2x,      0,    ],
        [ v0z-v2z,      0,      v2x-v0x,   p2z-p0z,      0,      p0x-p2x, ],
        [ v0y-v3y,   v3x-v0x,      0,      p3y-p0y,   p0x-p3x,      0,    ],
        [ v0z-v3z,      0,      v3x-v0x,   p3z-p0z,      0,      p0x-p3x, ],
    ]

    b = [
        p0x*v0y - p0y*v0x - p1x*v1y + p1y*v1x,
        p0x*v0z - p0z*v0x - p1x*v1z + p1z*v1x,
        p0x*v0y - p0y*v0x - p2x*v2y + p2y*v2x,
        p0x*v0z - p0z*v0x - p2x*v2z + p2z*v2x,
        p0x*v0y - p0y*v0x - p3x*v3y + p3y*v3x,
        p0x*v0z - p0z*v0x - p3x*v3z + p3z*v3x,
    ]

    pRx, pRy, pRz, vRx, vRy, vRz = cramer(A, b)
    return Ray(
        vec3(pRx, pRy, pRz),
        vec3(vRx, vRy, vRz),
    )

def det(m):
    """ Determinant of m """
    # base case
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    result = 0
    for c in range(len(m)):
        # Make a sub-matrix by removing row 0 and column c
        sub_mat = [row[:c] + row[c+1:] for row in m[1:]]
        # Alternate signs and recursively calculate the determinant
        result += ((-1) ** c) * m[0][c] * det(sub_mat)
    return result

def cramer(A, b):
    """ Solves matrix equation Ax=b using Cramer's rule and returns the vector x """
    x = []
    detA = det(A)
    if detA == 0:
        raise ValueError("Zero determinant")

    for c in range(len(b)):
        # Make a copy of the matrix
        Ai = deepcopy(A)

        # Replace the ith column with b
        for r in range(len(A)):
            Ai[r][c] = b[r]

        # Append det(Ai) / det(A) to the answer vector
        x.append(det(Ai) / detA)

    return x

def parse_ray(line):
    pos, vel = line.split(' @ ', 1)
    pos = pos.strip().split(', ')
    vel = vel.strip().split(', ')

    px, py, pz = map(int, pos)
    vx, vy, vz = map(int, vel)

    return Ray(
        vec3(px, py, pz),
        vec3(vx, vy, vz),
    )

if __name__ == '__main__':
    with open('input.txt') as file:
        stones = [parse_ray(line) for line in file.readlines()]
        rock = get_rock(stones)
        print(rock)
        print('Answer:', rock.pos.x + rock.pos.y + rock.pos.z)
