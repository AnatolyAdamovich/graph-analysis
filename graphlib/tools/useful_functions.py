'''Функции для анализа графов и др.'''
from ..algorithms import BFS_geodesic, BFS_search


# плотность графа
def density(graph):
    e = graph.edges_count
    k_graph_edges = 0.5 * e * (e - 1)
    return e / k_graph_edges


# доля вершин в подграфе
def proportion_of_subgraph(subgraph, graph):
    return subgraph.nodes_count / graph.nodes_count


def geodesic_percentile_approximate(graph, number=500, percent=50):
    nodes = list(graph.selection(x=number))
    list_with_distances = []
    while nodes:
        u = nodes.pop()
        for v in nodes:
            d = BFS_search(graph, start_u=u, finish_v=v, length=True)
            list_with_distances.append(d)
    list_with_distances.sort()
    n = len(list_with_distances)
    index_of_percentile = round(n*(percent/100))
    return list_with_distances[index_of_percentile]




# диаметр графа
def diameter(graph, with_node=False, approximate=False):
    d = -1
    node = -1
    for u in graph.nodes:
        current_geo = BFS_geodesic(graph, u, largest=True)
        if current_geo > d:
            node = u
            d = current_geo
    if with_node:
        return d, node
    return d


# оценка диаметра
def diameter_approximate(graph, number=500, nodes=None, with_nodes=False):
    if nodes is None:
        nodes = list(graph.selection(x=number))
    else:
        nodes = list(nodes)
    d = 0
    node1, node2 = None, None
    for i in range(len(nodes)-1):
        u = nodes[i]
        for j in range(i+1, len(nodes)):
            v = nodes[j]
            current_distance = BFS_search(graph, u, v, length=True)
            if current_distance > d:
                d = current_distance
                node1, node2 = u, v
    if with_nodes:
        return d, node1, node2
    return d


# радиус графа
def radius(graph, with_central=False):
    r = 1e+10
    node = -1
    for u in graph.nodes:
        current_geo = BFS_geodesic(graph, u, largest=True)
        if current_geo < r:
            node = u
            r = current_geo
    if with_central:
        # возвращение "центральной" вершины графа
        return r, node
    return r


# оценка радиуса (наименьшее расстояние из наибольших)
def radius_approximate(graph,  number=500, nodes=None, with_nodes=False):
    if nodes is None:
        nodes = list(graph.selection(x=number))
    else:
        nodes = list(nodes)
    r = 1000000000
    node1, node2 = None, None
    for u in nodes:
        max_geodesic_dist_for_u = 0
        tmp_node = None
        # поиск наибольшего расстояния между 'u' и другой вершиной
        for v in nodes:
            geo_dist = BFS_search(graph, start_u=u, finish_v=v, length=True)
            if geo_dist > max_geodesic_dist_for_u:
                max_geodesic_dist_for_u = geo_dist
                tmp_node = v
        # поиск наименьшего среди наибольших
        if max_geodesic_dist_for_u < r:
            node1, node2 = u, tmp_node
            r = max_geodesic_dist_for_u
    if with_nodes:
        return r, node1, node2
    return r


# Пусть степень вершины - это случайная величина.
# Считаем относительные частоты. Например, всего N вершин.
# Среди них M вершин имеют степень равную 10. Значит
# M/N  - вероятность того, что вершина имеет степень равную 10
# и т.д.
def degrees_probability(nodes):
    pass



