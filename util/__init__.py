import math
import random
from collections import deque
from math import inf
from queue import PriorityQueue
from typing import Callable, Generic, Hashable, Iterable, Self, TypeVar, Union

T = TypeVar('T')
class Bag(Generic[T]):
    def push(self, item: T) -> None:
        raise NotImplemented

    def pop(self) -> T:
        raise NotImplemented

    def __len__(self) -> int:
        raise NotImplemented

    def __bool__(self) -> bool:
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

Vertex = TypeVar('Vertex', bound=Hashable) # Vertex type
Weight = Union[int, float] # Edge weight type
class Graph(Generic[Vertex]):
    def __init__(self):
        self.vertices: set[Vertex] = set()
        self.edges: dict[Vertex, dict[Vertex, Weight]] = dict()
        self._total_weight = 0

    def add_edge(self, u: Vertex, v: Vertex, weight: Weight) -> None:
        self.vertices.add(u)
        self.vertices.add(v)
        if u not in self.edges:
            self.edges[u] = {}
        self.edges[u][v] = weight
        self._total_weight += weight

    def add_undirected_edge(self, u: Vertex, v: Vertex, weight: Weight) -> None:
        self.add_edge(u, v, weight)
        self.add_edge(v, u, weight)

    def get_neighbors(self, u: Vertex, d: Weight=0) -> Iterable[tuple[Vertex, Weight]]:
        return self.edges.get(u, {}).items()

    def has_edge(self, u: Vertex, v: Vertex) -> bool:
        return v in self.edges.get(u, {})

    def get_weight(self, u: Vertex, v: Vertex) -> Weight:
        return self.edges.get(u, {}).get(v, inf)

    def set_weight(self, u: Vertex, v: Vertex, weight: Weight) -> None:
        self._total_weight -= self.edges[u][v]
        self._total_weight += weight
        self.edges[u][v] = weight

    def iter_edges(self) -> Iterable[tuple[Vertex, Vertex, Weight]]:
        for u, nbrs in self.edges.items():
            for v, weight in nbrs.items():
                yield u, v, weight

    def reversed(self) -> Self:
        g = Graph()
        for u, nbrs in self.edges.items():
            for v, weight in nbrs.items():
                g.add_edge(v, u, weight)
        return g

    def delete_vertex(self, u: Vertex) -> None:
        # remove edges v -> u
        for v, weight in self.get_neighbors(u):
            self.edges.get(v, {}).pop(u, None)
            self._total_weight -= weight
        # remove edges u -> v
        nbrs = self.edges.pop(u, {})
        self._total_weight -= sum(nbrs.values())
        self.vertices.remove(u)

    def has_cycle(self, s: Vertex) -> bool:
        """ Returns true if there is a cycle reachable from s """
        marked = set()
        bag = Stack() # dfs
        bag.push(s)
        while bag:
            u = bag.pop()
            if u not in marked:
                marked.add(u)
                for v, _ in self.get_neighbors(u):
                    if v in marked:
                        return True
                    bag.push(v)
        return False

    def wfs(
            self,
            s: Vertex,
            bag: Bag[tuple[Vertex | None, Vertex, Weight]],
            on_marked: Callable[[Vertex, Weight], None]
    ) -> dict[Vertex, Vertex | None]:
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

    def _init_sssp(self, s: Vertex) -> tuple[dict[Vertex, Weight], dict[Vertex, Vertex | None]]:
        dist = {}
        pred = {}
        for v in self.vertices:
            dist[v] = inf
            pred[v] = None
        dist[s] = 0
        return dist, pred

    def dijkstra(self, s: Vertex) -> tuple[dict[Vertex, Weight], dict[Vertex, Vertex | None]]:
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
                relaxed_dist = u_dist + self.get_weight(u, v)
                if relaxed_dist < dist[v]:
                    dist[v] = relaxed_dist
                    pred[v] = u
                    pq.put((relaxed_dist, v))

        return dist, pred

    def path_weight(self, path: list[Vertex]) -> Weight:
        """ Given a path s ~> v (list of vertices along the path), returns the
            total weight of all edges along the path """
        weight = 0
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i+1]
            weight += self.get_weight(u, v)
        return weight

    @staticmethod
    def get_path(pred: dict[Vertex, Vertex | None], v: Vertex) -> list[Vertex]:
        """ Returns a path from s ~> v given a predecessor dict """
        path = []
        while v is not None:
            path.append(v)
            v = pred[v]
        path.reverse()
        return path

    def topo_sort_wfs(self, s: Vertex) -> list[Vertex]:
        """ Get a topological order for only vertices reachable from s """
        order = []
        self._top_sort_dfs(set(), order, s)
        order.reverse()
        return order

    def topo_sort(self) -> list[Vertex]:
        """ Get a topological order for this graph. Requires that the graph is a DAG """
        order = []
        marked = set()
        for u in self.vertices:
            if u not in marked:
                self._top_sort_dfs(marked, order, u)
        order.reverse()
        return order

    def _top_sort_dfs(self, marked: set[Vertex], order: list[Vertex], u: Vertex) -> None:
        """ Helper function for topo sorting """
        marked.add(u)
        for v, _ in self.get_neighbors(u):
            if v not in marked:
                self._top_sort_dfs(marked, order, v)
        order.append(u)

    def karger(self, run_until=None) -> tuple[set[Vertex], set[Vertex], int]:
        """
        Implementation of Karger's minimum cut algorithm. Returns two sets of vertices that partition
        the graph into two disconnected components with a minimum cut, as well as the number of cuts.

        The graph must be undirected and connected.
        """
        MergedVert = tuple[Vertex, ...]
        Edge = tuple[MergedVert, MergedVert]

        def contract(edges: list[Edge], s: MergedVert, t: MergedVert):
            """ Contracts an edge according to Karger's algorithm """
            st = s + t
            i = 0
            while i < len(edges):
                u, v = edges[i]
                if u == s and v == t or u == t and v == s:
                    # self loop, delete edge
                    edges[i], edges[-1] = edges[-1], edges[i]
                    edges.pop()
                    i -= 1
                elif u == s or u == t:
                    edges[i] = (st, v)
                elif v == s or v == t:
                    edges[i] = (st, u)
                i += 1

        edge_set = dict()
        for u, v, weight in self.iter_edges():
            if (v, u) not in edge_set:
                edge_set[(u, v)] = weight

        edges: list[Edge] = []
        for (u, v), weight in edge_set.items():
            for _ in range(weight):
                edges.append(((u,), (v,)))

        i = 1
        n = self.num_vertices()
        num_runs = math.ceil((n * (n - 1) / 2) * math.log(n))
        while True:
            edge_copy = edges.copy()
            for _ in range(self.num_vertices() - 2):
                s, t = random.choice(edge_copy)
                contract(edge_copy, s, t)

            print(f'Run {i}: {len(edge_copy)}')
            if i >= num_runs or (run_until is not None and len(edge_copy) <= run_until):
                result = edge_copy
                break
            i += 1

        c1, c2 = result[0]
        return set(c1), set(c2), len(result)

    def num_vertices(self) -> int:
        return len(self.vertices)

    def num_edges(self) -> int:
        e = 0
        for adj in self.edges.values():
            e += len(adj)
        return e

    def total_weight(self) -> Weight:
        # w = sum(w for _, _, w in self.iter_edges())
        # if w != self._total_weight:
        #     raise AssertionError(f"Expected {w} got {self._total_weight}")
        return self._total_weight

    def is_connected(self) -> bool:
        visited = set()
        def mark(v, _):
            visited.add(v)
        self.wfs(next(iter(self.vertices)), Stack(), mark)
        return visited == self.vertices

    def is_undirected(self) -> bool:
        for u, v, _ in self.iter_edges():
            if not self.has_edge(v, u):
                return False
        return True

    def is_unweighted(self) -> bool:
        return all(weight == 1 for _, _, weight in self.iter_edges())

    def copy(self) -> Self:
        g = Graph()
        for u, v, weight in self.iter_edges():
            g.add_edge(u, v, weight)
        return g

    def __str__(self) -> str:
        s = 'Graph {\n'
        for v, nbrs in self.edges.items():
            nbrs = ('{}:{}'.format(nbr, wgt) for nbr, wgt in nbrs.items())
            s += '\t{} -> {}\n'.format(v, ' '.join(nbrs))
        s += '}'
        return s