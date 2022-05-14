''' Поиск компонент слабой и сильной связности в графах '''
from .DFS import *


# компоненты слабой связности
def weakly_components(digraph, largest=False):
    graph = digraph.to_simple()
    return DFS_with_cc(graph, largest)


# компоненты сильной связности
# предпочтительнее использовать алгоритм Тарьяна (всего один обход в глубину)
def strongly_components_tarjan(digraph):
    time_in = {}     # время входа в вершину
    ret = {}         # куда можно вернуться из вершины
    used = set()         # вершины, для которых определена компонента
    queue_for_scc = []
    time = 0
    neighbors = {v: iter(digraph.neighbors_for_node(v))
                 for v in digraph.edges}

    for node in digraph.nodes:
        if node not in used:
            available_nodes = [node]
            while available_nodes:
                u = available_nodes[-1]
                if u not in time_in:
                    time += 1
                    time_in[u] = time
                leaf = True
                for v in neighbors[u]:
                    if v not in time_in:
                        available_nodes.append(v)
                        leaf = False
                        break  # берем ТОЛЬКО первую необследованную вершину
                if leaf:
                    ret[u] = time_in[u]
                    for v in digraph.neighbors_for_node(u):
                        if v not in used:
                            if time_in[v] > time_in[u]:
                                ret[u] = min([ret[u], ret[v]])
                            else:
                                ret[u] = min([ret[u], time_in[v]])
                    available_nodes.pop()
                    if ret[u] == time_in[u]:
                        scc = {u}
                        while queue_for_scc and time_in[queue_for_scc[-1]] > time_in[u]:
                            new_node_to_scc = queue_for_scc.pop()
                            scc.add(new_node_to_scc)
                        used.update(scc)
                        yield scc
                    else:
                        queue_for_scc.append(u)


# альтернатива - алгоритм Косарайю (два обхода в глубину + рекурсивный DFS)
def strongly_components_kosaraju(digraph):
    # расположение вершин в порядке убывания времени выхода
    time_in, time_out = DFS_with_times_recursive(digraph)
    time_out = sorted(list(time_out.items()), key=lambda elem: elem[1])
    order = list(map(lambda elem: elem[0], time_out))
    # транспонирование графа
    invert = digraph.invert()

    # поиск в глубину на транспонированном графе
    # с учетом порядка
    available_nodes = deque()
    visited = set()
    scc = dict()
    scc_num = 0
    while order:
        node = order.pop()
        if node not in visited:
            scc_num += 1
            scc[scc_num] = set()
            available_nodes.append(node)
            while available_nodes:
                u = available_nodes.pop()
                for v in invert.neighbors_for_node(u):
                    if v not in visited:
                        available_nodes.append(v)
                        visited.add(v)
                scc[scc_num].add(u)
                visited.add(u)
    return scc


# метаграф
