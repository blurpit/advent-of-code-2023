from collections import deque


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
        self.vertices = set()
        self.edges = dict()

    def add_edge(self, v, w):
        self.vertices.add(v)
        self.vertices.add(w)
        if v not in self.edges:
            self.edges[v] = []
        self.edges[v].append(w)

    def get_neighbors(self, v):
        return self.edges.get(v, [])

    def has_edge(self, v, w):
        return w in self.edges.get(v, ())

    def wfs(self, s, bag: Bag, on_marked):
        marked = set()
        bag.push(s)
        while bag:
            v = bag.pop()
            if v not in marked:
                marked.add(v)
                on_marked(v)
                for w in self.get_neighbors(v):
                    bag.push(w)

    def __str__(self):
        s = 'Graph {\n'
        for v, nbrs in self.edges.items():
            s += '\t{} -> {}\n'.format(v, ' '.join(map(str, nbrs)))
        s += '}'
        return s