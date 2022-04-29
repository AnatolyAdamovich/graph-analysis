'''
Поиск в глубину.

Может быть использован для поиска компонент связности в графе
'''
from collections import deque


def DFS_with_cc(graph, largest=False):
    """Поиск в глубину с нахождением компонент связности.

        Parameters
        ----------
        graph : Graph
            Граф
        largest : bool
                Если True, то возвращается индекс наибольшей компоненты связности

    Возвращает:
        - количество компонент связности
        - компоненты связности
    """
    available_nodes = deque()
    visited = set()
    cc = dict()
    cc_num = 0

    for node in graph.nodes:
        if node not in visited:
            cc_num += 1
            cc[cc_num] = set()
            available_nodes.append(node)
            while available_nodes:
                u = available_nodes.pop()
                for v in graph.neighbors_for_node(u):
                    if v not in visited:
                        available_nodes.append(v)
                        visited.add(v)
                cc[cc_num].add(u)
                visited.add(u)
    if largest:
        max_component_number = max(cc, key=lambda num: len(cc[num]))
        return cc_num, max_component_number, cc
    return cc_num, cc


def DFS_with_times_recursive(graph):
    # рекурсивный DFS с временными метками
    time_in = dict()     # время входа в вершину
    time_out = dict()    # время выхода из вершины
    time = 1
    visited = set()

    def explore(node):
        nonlocal time  # для изменения локальной переменной функции на уровень выше
        visited.add(node)
        time_in[node] = time
        time += 1

        for adj_node in graph.neighbors_for_node(node):
            if adj_node not in visited:
                explore(adj_node)
        time_out[node] = time
        time += 1

    for u in graph.nodes:
        if u not in visited:
            explore(u)
    return time_in, time_out
