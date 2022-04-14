'''
Поиск в глубину.

Может быть использован для поиска компонент связности в графе
'''
from collections import deque


def DFS_with_cc(graph, largest=False):
    # поиск в глубину с подсчетом компонент связности
    available_nodes = deque()
    visited = set()

    cc = dict()
    ccnum = 0

    for node in graph.nodes:
        if node not in visited:
            ccnum += 1
            cc[ccnum] = set()
            available_nodes.append(node)
            while available_nodes:
                u = available_nodes.pop()
                for v in graph.neighbors_for_node(u):
                    if v not in visited:
                        available_nodes.append(v)
                        visited.add(v)
                cc[ccnum].add(u)
                visited.add(u)
    if largest:
        max_component_number = max(cc, key=lambda num: len(cc[num]))
        return ccnum, max_component_number, cc
    return ccnum, cc
