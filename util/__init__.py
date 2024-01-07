from collections import deque
from math import inf
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
        self.vertices = set()
        self.edges = dict()

    def add_edge(self, u, v, weight):
        self.vertices.add(u)
        self.vertices.add(v)
        if u not in self.edges:
            self.edges[u] = {}
        self.edges[u][v] = weight

    def get_neighbors(self, u, d=None):
        return self.edges.get(u, {}).items()

    def has_edge(self, u, v):
        return v in self.edges.get(u, {})

    def edge_weight(self, u, v):
        return self.edges.get(u, {}).get(v, inf)

    def reversed(self):
        g = Graph()
        for u, nbrs in self.edges.items():
            for v, weight in nbrs.items():
                g.add_edge(v, u, weight)
        return g

    def delete_vertex(self, u):
        # remove edges v -> u
        for v, _ in self.get_neighbors(u):
            self.edges.get(v, {}).pop(u, None)
        # remove edges u -> v
        self.edges.pop(u, None)

    def wfs(self, s, bag: Bag, on_marked):
        marked = set()
        bag.push((None, s, 0))
        pred = dict()
        while bag:
            p, u, d = bag.pop()
            if u not in marked:
                marked.add(u)
                pred[u] = p
                on_marked(u, d)
                for v, cost in self.get_neighbors(u, d):
                    bag.push((u, v, d + cost))
        return pred

    def _init_sssp(self, s):
        dist = {}
        pred = {}
        for v in self.vertices:
            dist[v] = inf
            pred[v] = None
        dist[s] = 0
        return dist, pred

    def dijkstra(self, s):
        """
        Implementation of Dijkstra's single source shortest path algorithm starting at vertex s.
        Returns (dist, pred). Dist is a dictionary mapping each vertex to the distance to s. Pred
        is a dictionary mapping each vertex to its predecessor vertex in the shortest path from s.
        Requires non-negative edge weights!!! """
        dist, pred = self._init_sssp(s)

        pq = PriorityQueue()
        for v in self.vertices:
            pq.put((dist[v], v))

        while pq.qsize() > 0:
            _, u = pq.get()
            u_dist = dist[u]
            for v, weight in self.get_neighbors(u):
                # u->v is tense if dist(u) + w(u->v) < dist(v)
                relaxed_dist = u_dist + self.edge_weight(u, v)
                if relaxed_dist < dist[v]:
                    dist[v] = relaxed_dist
                    pred[v] = u
                    pq.put((relaxed_dist, v))

        return dist, pred

    def path_weight(self, path):
        """ Given a path s ~> v (list of vertices along the path), returns the
            total weight of all edges along the path """
        weight = 0
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i+1]
            weight += self.edge_weight(u, v)
        return weight

    @staticmethod
    def get_path(pred, v):
        """ Returns a path from s ~> v given a predecessor dict """
        path = []
        while v is not None:
            path.append(v)
            v = pred[v]
        path.reverse()
        return path

    def topo_sort_wfs(self, s):
        """ Get a topological order for only vertices reachable from s """
        order = []
        self._top_sort_dfs(set(), order, s)
        order.reverse()
        return order

    def topo_sort(self):
        """ Get a topological order for this graph. Requires that the graph is a DAG """
        order = []
        marked = set()
        for u in self.vertices:
            if u not in marked:
                self._top_sort_dfs(marked, order, u)
        order.reverse()
        return order

    def _top_sort_dfs(self, marked, order, u):
        """ Helper function for topo sorting """
        marked.add(u)
        for v, _ in self.get_neighbors(u):
            if v not in marked:
                self._top_sort_dfs(marked, order, v)
        order.append(u)

    def num_vertices(self):
        return len(self.vertices)

    def num_edges(self):
        e = 0
        for adj in self.edges.values():
            e += len(adj)
        return e

    def __str__(self):
        s = 'Graph {\n'
        for v, nbrs in self.edges.items():
            s += '\t{} -> {}\n'.format(v, ' '.join(map(str, nbrs)))
        s += '}'
        return s