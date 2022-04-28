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
