'''Cтруктура данных для неориентированного невзвешенного графа'''


class Graph:
    def __init__(self, name='null', nodes=None):
        self._name = name
        if nodes is None:
            self._nodes = set()
        else:
            self._nodes = set(nodes)
        # список смежности для каждой вершины;
        self._edges = dict([(node, []) for node in self._nodes])

    @property
    def nodes(self):
        # вершины графа
        return self._nodes

    @property
    def nodes_count(self):
        # число вершин в графе
        return len(self._nodes)

    @property
    def edges_count(self):
        # число ребер
        # Лемма: [ sum(deg(node)) foreach node in G ] = 2 * |E|
        return int((sum(map(len, self._edges.values()))) / 2)

    def add_node(self, u):
        # добавление вершины
        self._nodes.add(u)
        self._edges[u] = []

    def add_edge(self, u, v):
        # добавление ребра
        if u not in self._nodes:
            self.add_node(u)
        if v not in self._nodes:
            self.add_node(v)
        if v not in self._edges[u]:
            self._edges[u].append(v)
            self._edges[v].append(u)

    def neighbors_for_node(self, u):
        return self._edges[u]

    def __str__(self):
        result = f'Graph <{self._name}> with {self.nodes_count} nodes and {self.edges_count} edges'
        return result

    #def subgraph(self):