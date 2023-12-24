from collections import deque
from queue import PriorityQueue


class Bag:
    def push(self, item):
        raise NotImplemented

    def pop(self):
        raise NotImplemented

    def __len__(self):
        raise NotImplemented

    def __bool__(self):
        return len(self) > 0

class Stack(Bag):
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        return self._data.pop()

    def __len__(self):
        return len(self._data)

    def __bool__(self):
        return len(self) > 0

    def __str__(self):
        return str(self._data)

class Queue(Bag):
    def __init__(self):
        self._data = deque()

    def push(self, item):
        self._data.append(item)

    def pop(self):
        return self._data.popleft()

    def __len__(self):
        return len(self._data)

    def __bool__(self):
        return len(self) > 0

    def __str__(self):
        return str(self._data)


class Graph:
    def __init__(self):
        self.edges = dict()

    def add_edge(self, u, v, weight):
        if u not in self.edges:
            self.edges[u] = {}
        self.edges[u][v] = weight

    def get_neighbors(self, u):
        return self.edges.get(u, {}).items()

    def has_edge(self, v, w):
        return w in self.edges.get(v, {})

    def wfs(self, s, bag: Bag, on_marked):
        marked = set()
        bag.push((None, s))
        pred = dict()
        while bag:
            p, u = bag.pop()
            if u not in marked:
                marked.add(u)
                pred[u] = p
                on_marked(u)
                for v, _ in self.get_neighbors(u):
                    bag.push((u, v))
        return pred

    def __str__(self):
        s = 'Graph {\n'
        for v, nbrs in self.edges.items():
            s += '\t{} -> {}\n'.format(v, ' '.join(map(str, nbrs)))
        s += '}'
        return s