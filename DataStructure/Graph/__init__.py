from copy import deepcopy
from DataStructure.Heap import AdaptableHeapPriorityQueue


class Vertex(object):
    __slots__ = '_element'

    def __init__(self, x):
        self._element = x

    def element(self):
        return self._element

    def __hash__(self):
        return hash(id(self))


class Edge(object):
    __slots__ = '_origin', '_destination', '_element'

    def __init__(self, u, v, x):
        self._origin = u
        self._destination = v
        self._element = x

    def endpoints(self):
        return self._origin, self._destination

    def opposite(self, v):
        return self._destination if v is self._origin else self._origin

    def element(self):
        return self._element

    def __hash__(self):
        return hash((self._origin, self._destination))


class Graph(object):
    def __init__(self, directed=False):
        self._outgoing = {}
        self._incoming = {} if directed else self._outgoing

    def is_directed(self):
        return self._incoming is not self._outgoing

    def vertex_count(self):
        return len(self._outgoing)

    def vertices(self):
        return self._outgoing.keys()

    def edge_count(self):
        _total = sum(len(self._outgoing[v]) for v in self._outgoing)
        return _total if self.is_directed() else _total // 2

    def edges(self):
        _result = set()
        for secondary_map in self._outgoing.values():
            _result.update(secondary_map.values())

        return _result

    def get_edge(self, u, v):
        return self._outgoing[u].get(v)

    def degree(self, v, outgoing=True):
        _adj = self._outgoing if outgoing else self._incoming
        return len(_adj[v])

    def incident_edges(self, v, outgoing=True):
        _adj = self._outgoing if outgoing else self._incoming
        for edge in _adj[v].values():
            yield edge

    def insert_vertex(self, x=None):
        v = Vertex(x)
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}

        return v

    def insert_edge(self, u, v, x=None):
        e = Edge(u, v, x)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e


def dfs(graph, u, visited):
    """
    ns <= n 顶点s可达顶点数
    ms <= m 这些顶点的入射边数
    O(ns + ms)
    :param graph:
    :param u:
    :param visited:
    :return:
    """

    print(u.element())
    for edge in graph.incident_edges(u):
        v = edge.opposite(u)
        if v not in visited:
            visited[v] = edge
            dfs(graph, v, visited)


def construct_path(u, v, visited):
    _path = []
    if v in visited:
        _path.append(v)
        _walk = v
        while _walk is not u:
            _edge = visited[_walk]
            _parent = _edge.opposite(_walk)
            _path.append(_parent)
            _walk = _parent

        _path.reverse()

    return _path


def dfs_complete(graph):
    _forest = {}
    for u in graph.vertices():
        if u not in _forest:
            _forest[u] = None
            dfs(graph, u, _forest)

    return _forest


def bfs(graph, s, visited):
    """
    ns <= n 顶点s可达顶点数
    ms <= m 这些顶点的入射边数
    O(ns + ms)
    :param graph:
    :param s:
    :param visited:
    :return:
    """

    _level = [s]
    while len(_level) > 0:
        _next_level = []
        for u in _level:
            for e in graph.incident_edges(u):
                v = e.opposite(u)
                if v not in visited:
                    visited[v] = e
                    _next_level.append(v)

        _level = _next_level


def floyd_warshall(graph):
    _closure = deepcopy(graph)
    _vertices = list(_closure.vertices())
    _len = len(_vertices)
    for k in range(_len):
        for i in range(_len):
            if i != k and _closure.get_edge(_vertices[i], _vertices[k]) is not None:
                for j in range(_len):
                    if i != j != k and _closure.get_edge(_vertices[k], _vertices[j]) is not None:
                        if _closure.get_edge(_vertices[i], _vertices[j]) is None:
                            _closure.insert_edge(_vertices[i], _vertices[j])

    return _closure


def topological_sort(graph):
    """
    拓扑排序
    O(n)
    :param graph:
    :return:
    """
    
    _topological = []
    _ready = []
    _in_degree_count = {}
    for u in graph.vertices():
        _in_degree_count[u] = graph.degree(u, False)
        if _in_degree_count[u] == 0:
            _ready.append(u)

    while len(_ready) > 0:
        u = _ready.pop()
        _topological.append(u)
        for e in graph.incident_edges(u):
            v = e.opposite(u)
            _in_degree_count[v] -= 1
            if _in_degree_count[v] == 0:
                _ready.append(v)

    return _topological


def shortest_path_lengths(graph, source):
    """
    迪克斯特拉算法
    :param graph:
    :param source:
    :return:
    """

    d = {}
    cloud = {}
    pq = AdaptableHeapPriorityQueue()
    pq_locator = {}

    for v in graph.vertices():
        if v is source:
            d[v] = 0
        else:
            d[v] = float('inf')  # 默认为无限大

        pq_locator[v] = pq.add(d[v], v)

    while not pq.is_empty():
        key, u = pq.remove_min()
        cloud[u] = key
        del pq_locator[u]
        for e in graph.incident_edges(u):
            v = e.opposite(u)
            if v not in cloud:
                wgt = e.element()
                if d[u] + wgt < d[v]:
                    d[v] = d[u] + wgt
                    pq.update(pq_locator[v], d[v], v)

    return cloud


def shortest_path_tree(graph, source, d_map):
    _tree = {}
    for v in d_map:
        if v is not source:
            for e in graph.incident_edges(v, False):
                u = e.opposite(v)
                wgt = e.element()
                if d_map[v] == d_map[u] + wgt:
                    _tree[v] = e

    return _tree


def mst_prim_jarnik(graph):
    """
    普里姆算法
    :param graph: 
    :return: 
    """
    
    d = {}
    _tree = []
    pq = AdaptableHeapPriorityQueue()
    pq_locator = {}
    
    for v in graph.vertices():
        if len(d) == 0:
            d[v] = 0
        else:
            d[v] = float('inf')
            
        pq_locator[v] = pq.add(d[v], (v, None))

    while not pq.is_empty():
        key, value = pq.remove_min()
        u, edge = value
        del pq_locator[u]
        if edge is not None:
            _tree.append(edge)

        for _link in graph.incident_edges(u):
            v = _link.opposite(u)
            if v in pq_locator:
                wgt = _link.element()
                if wgt < d[v]:
                    d[v] = wgt
                    pq.update(pq_locator[v], d[v], (v, _link))
                        
    return _tree


class Partition(object):
    class Position(object):
        __slots__ = '_container', '_element', 'size', 'parent'

        def __init__(self, container, element):
            self._container = container
            self._element = element
            self.size = 1
            self.parent = self

        def element(self):
            return self._element

    def make_group(self, element):
        return self.Position(self, element)

    def find(self, position):
        if position.parent != position:
            position.parent = self.find(position.parent)

        return position.parent

    def union(self, position1, position2):
        a = self.find(position1)
        b = self.find(position2)
        if a is not b:
            if a.size > b.size:
                b.parent = a
                a.size += b.size
            else:
                a.parent = b
                b.size += a.size


def mst_kruskal(graph):
    """
    克鲁斯卡尔算法
    :param graph:
    :return:
    """

    _tree = []
    pq = AdaptableHeapPriorityQueue()
    _forest = Partition()
    _position = {}

    for v in graph.vertices():
        _position[v] = _forest.make_group(v)

    for e in graph.edges():
        pq.add(e.element(), e)

    _size = graph.vertex_count()
    while len(_tree) != _size - 1 and not pq.is_empty():
        weight, edge = pq.remove_min()
        u, v = edge.endpoints()
        a = _forest.find(_position[u])
        b = _forest.find(_position[v])
        if a != b:
            _tree.append(edge)
            _forest.union(a, b)

    return _tree


if __name__ == '__main__':
    _n = 10
    _g = Graph()
    for _i in range(_n):
        _g.insert_vertex(_i)

    _v_l = list(_g.vertices())
    for _i in range(_n):
        _g.insert_edge(_v_l[_i], _v_l[(_i + 1) % _n], _i)

    _visited = {_v_l[0]: None}
    dfs(_g, _v_l[0], _visited)
    construct_path(_v_l[0], _v_l[9], _visited)
    print(_n == len(_visited))
    dfs_complete(_g)

    _d_map = shortest_path_lengths(_g, _v_l[0])
    shortest_path_tree(_g, _v_l[0], _d_map)
    
    mst_prim_jarnik(_g)
    mst_kruskal(_g)
