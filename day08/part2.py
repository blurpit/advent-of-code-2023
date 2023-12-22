import itertools
import math
import re

from util import Graph


def build_graph(edges):
    g = Graph()
    for root, left, right in edges:
        g.add_edge(root, left)
        g.add_edge(root, right)
    return g

def parse_edge(line):
    m = re.match(r'(\w{3}) = \((\w{3}), (\w{3})\)', line)
    root = m.group(1)
    left = m.group(2)
    right = m.group(3)
    return root, left, right

def get_all_a(vertices):
    return [
        v for v in vertices
        if v.endswith('A')
    ]

def path_length(graph, start, instructions):
    instructions = itertools.cycle(instructions)
    vertex = start
    steps = 0
    while not vertex[-1] == 'Z':
        instruction = next(instructions)
        left, right = graph.get_neighbors(vertex)
        if instruction == 'L':
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
        paths = [path_length(g, v, instructions) for v in get_all_a(g.vertices)]
        n = math.lcm(*paths)
        print(n)
