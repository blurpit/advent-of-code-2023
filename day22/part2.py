from math import inf

from util import Graph, Queue


class Block:
    def __init__(self, brick, x, y, z):
        self.brick = brick
        self.x = x
        self.y = y
        self.z = z

    @property
    def pos(self):
        return self.x, self.y, self.z

    def drop(self):
        self.brick.drop()

    def __repr__(self):
        return f'Block({self.x}, {self.y}, {self.z})'

class Brick:
    def __init__(self, line):
        start, end = line.split('~', 1)
        x1, y1, z1 = map(int, start.split(','))
        x2, y2, z2 = map(int, end.split(','))
        self.blocks = []
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    block = Block(self, x, y, z)
                    self.blocks.append(block)
        self.letter = next_letter()
        self._dropped = False

    def drop(self):
        """ drop the brick """
        # avoid dropping vertical bricks more than once
        if self._dropped:
            return
        self._dropped = True

        drop_amount = self.get_drop_amount()
        for block in self.blocks:
            # move block down by drop_amount
            del grid[block.pos]
            block.z -= drop_amount
            grid[block.pos] = block

    def get_drop_amount(self):
        """ number of z's to move this brick down by to drop it """
        # find a block with highest z underneath the brick
        z_start = min(b.z for b in self.blocks)
        for z in range(z_start - 1, 0, -1):
            for block in self.blocks:
                block2 = grid.get((block.x, block.y, z))
                if block2:
                    return z_start - z - 1
        # nothing underneath, drop all the way to z=1
        return z_start - 1

    def get_supports(self):
        """ returns a set of bricks this brick is supported by """
        # check for blocks 1 space beneath this brick
        supports = set()
        for block in self.blocks:
            block2 = grid.get((block.x, block.y, block.z - 1))
            if block2 and block2.brick is not self:
                supports.add(block2.brick)
        return supports

    def __repr__(self):
        return str(self.letter)

def next_letter():
    global letter
    tmp = letter
    letter = chr(ord(letter) + 1)
    return tmp

def get_dimensions():
    min_x = inf
    max_x = -inf
    min_y = inf
    max_y = -inf
    min_z = inf
    max_z = -inf
    for pos in grid.keys():
        min_x = min(min_x, pos[0])
        max_x = max(max_x, pos[0])
        min_y = min(min_y, pos[1])
        max_y = max(max_y, pos[1])
        min_z = min(min_z, pos[2])
        max_z = max(max_z, pos[2])
    width = max_x - min_x + 1
    depth = max_y - min_y + 1
    height = max_z - min_z + 1
    return width, depth, height

def print_grid():
    width, depth, height = get_dimensions()
    x_grid = [['.'] * width for _ in range(height)]
    y_grid = [['.'] * depth for _ in range(height)]

    for block in grid.values():
        x, y, z = block.pos
        letter = str(block.brick.letter)
        if x_grid[height-z][x] not in (letter, '.'):
            x_grid[height-z][x] = '?'
        else:
            x_grid[height-z][x] = letter

        if y_grid[height-z][y] not in (letter, '.'):
            y_grid[height-z][y] = '?'
        else:
            y_grid[height-z][y] = letter

    print('x')
    for r, row in enumerate(x_grid):
        print(''.join(row) + ' ' + str(height - r))
    print('-' * width + ' 0 z')
    print()

    print('y')
    for r, row in enumerate(y_grid):
        print(''.join(row) + ' ' + str(height - r))
    print('-' * width + ' 0 z')
    print()

if __name__ == '__main__':
    with open('input.txt') as file:
        letter = 'A'
        grid = {}
        brick_set = set()
        for line in file.readlines():
            brick = Brick(line)
            brick_set.add(brick)
            for block in brick.blocks:
                grid[block.pos] = block

        print_grid()

        # Drop bricks in order of lowest z value first
        print('Dropping...')
        sorted_blocks = sorted(grid.values(), key=lambda b: b.z)
        for b in sorted_blocks:
            b.drop()
        print_grid()

        # Build a support graph and reverse support graph. Each edge A->B in the
        # support graph means brick A is underneath brick B and supports it.
        support_graph = Graph()
        for brick in brick_set:
            supports = brick.get_supports()
            for support in supports:
                support_graph.add_edge(support, brick, 1)
        support_graph_rev = support_graph.reversed()

        answer = 0

        # For each starting brick s, count how many bricks would fall if s were
        # disintegrated. To do this, iterate the graph in topological order, and
        # for each brick, keep track of how many supporting bricks it has lost.
        # If a brick has lost all its supports, add it to the answer.
        for s in support_graph.vertices:
            # Topological order for vertices reachable from s
            topo_order = support_graph.topo_sort_wfs(s)
            # Mapping of each vertex to how many supporting bricks it has lost
            supp_lost = {}
            # Number of bricks that would fall if s were removed
            fallen = 0

            for brick in topo_order:
                # Check if this brick has lost all its supports
                num_supports = len(support_graph_rev.get_neighbors(brick))
                if brick is s or supp_lost.get(brick, 0) == num_supports:
                    # Increment fallen and remove one support for all edges
                    # brick->brick2
                    fallen += 1
                    for brick2, _ in support_graph.get_neighbors(brick):
                        supp_lost[brick2] = supp_lost.get(brick2, 0) + 1

            # Add fallen to answer. Remove one because we don't want to count
            # the starting brick s.
            print(s, fallen-1, sep='\t')
            answer += fallen-1

        print('Answer:', answer)
