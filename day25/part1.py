from util import Graph


def parse_graph(text):
    g = Graph()
    for line in text.splitlines():
        u, nbrs = line.split(': ')
        for v in nbrs.split():
            g.add_edge(u, v, 1)
            g.add_edge(v, u, 1)
    return g

if __name__ == '__main__':
    with open('input.txt') as file:
        graph = parse_graph(file.read())
        print(graph)
        c1, c2, cuts = graph.karger(run_until=3)
        print(c1)
        print(c2)
        print('Answer:', len(c1) * len(c2))

    # graph = Graph()
    # graph.add_undirected_edge('s', 't', 3)
    # graph.add_undirected_edge('s', 'a', 2)
    # graph.add_undirected_edge('s', 'b', 1)
    # graph.add_undirected_edge('s', 'c', 1)
    # graph.add_undirected_edge('t', 'a', 4)
    # graph.add_undirected_edge('t', 'd', 1)
    # graph.add_undirected_edge('a', 'b', 1)
    # print(graph)
    # edges = graph.karger()
    # for e in edges:
    #     print(e)


