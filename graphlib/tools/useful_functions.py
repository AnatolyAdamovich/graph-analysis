'''Функции для анализа графов и др.'''


# плотность графа
def density(graph):
    e = graph.edges_count
    k_graph_edges = 0.5 * e * (e - 1)
    return e / k_graph_edges


# доля вершин в подграфе
def proportion_of_subgraph(subgraph, graph):
    return subgraph.nodes_count / graph.nodes_count

