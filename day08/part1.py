import itertools
import re

from util import Graph


def build_graph(edges):
    g = Graph()
    for root, left, right in edges:
        g.add_edge(root, left, 1)
        g.add_edge(root, right, 1)
    return g

def parse_edge(line):
    m = re.match(r'(\w{3}) = \((\w{3}), (\w{3})\)', line)
    root = m.group(1)
    left = m.group(2)
    right = m.group(3)
    return root, left, right

def get_left_right(neighbors):
    if len(neighbors) == 2:
        (left, _), (right, _) = neighbors
    else:
        (left, _), = neighbors
        right = left
    return left, right

def follow_instructions(graph, instructions):
    instructions = itertools.cycle(instructions)
    steps = 0
    vertex = 'AAA'
    while vertex != 'ZZZ':
        left, right = get_left_right(graph.get_neighbors(vertex))
        if next(instructions) == 'L':
            vertex = left
        else:
            vertex = right
        steps += 1
    return steps

if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        instructions = file.readline().strip()
        file.readline() # blank line
        edges = [parse_edge(line) for line in file.readlines()]
        g = build_graph(edges)
        steps = follow_instructions(g, instructions)
        print(steps)
