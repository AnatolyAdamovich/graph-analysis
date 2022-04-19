'''Cтруктура данных для неориентированного невзвешенного графа'''
import random


class Graph:
    def __init__(self, name='null', nodes=None, edges=None):
        self.name = name

        if nodes is None:
            self._nodes = set()
        else:
            self._nodes = set(nodes)

        if edges is not None:
            if type(edges) is dict:
                self._edges = edges
            elif type(edges) is list:
                # список смежности для каждой вершины;
                self._edges = dict([(node, []) for node in self._nodes])
                for (u, v) in edges:
                    self.add_edge(u, v)
        else:
            # список смежности для каждой вершины;
            self._edges = dict([(node, []) for node in self._nodes])

    @property
    def nodes(self):
        # вершины графа
        return self._nodes

    @property
    def edges(self):
        # список смежности для каждой вершины графа
        return self._edges

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
        if u not in self._nodes:
            self._nodes.add(u)
            self._edges[u] = []

    def add_nodes(self, list_with_nodes):
        # добавление вершины
        for u in list_with_nodes:
            self.add_node(u)

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
        result = f'Graph <{self.name}> with {self.nodes_count} nodes and {self.edges_count} edges'
        return result

    def random_selection(self, x):
        # случайный выбор x вершин из графа
        new_nodes = random.sample(self.nodes, k=x)
        return new_nodes

    def node_degrees(self):
        # возвращение вершин со степенью смежности (list with tuples)
        deg = list(map(lambda node: (node[0], len(node[1])), self.edges.items()))
        return sorted(deg, key=lambda node: node[1], reverse=True)

    def random_removing(self, k, most_degree=False):
        # удаление k случайных вершин в графе
        if most_degree:
            nodes_for_removing = self.node_degrees()
            nodes_for_removing = set(map(lambda node: node[0], nodes_for_removing[:k]))
            saved_nodes = self.nodes - nodes_for_removing
            return self.subgraph(nodes=saved_nodes)

        saved_nodes = self.random_selection(self.nodes_count - k)
        return self.subgraph(nodes=saved_nodes)

    def subgraph(self, nodes=None, x=3):
        # подграф исходного графа

        if nodes is None:
            # вершины выбираются случайным образом
            sub_nodes = set(self.random_selection(x))
        else:
            # с определенными вершинами
            sub_nodes = set(nodes)

        sub_edges = dict([(node, [adj_node for adj_node in self._edges[node] if adj_node in sub_nodes])
                          for node in sub_nodes])

        subgraph = Graph(name='subgraph::' + self.name,
                         nodes=sub_nodes,
                         edges=sub_edges)
        return subgraph
