'''
Поиск в ширину.

Может быть использован для поиска кратчайшего пути
между двумя вершинами в невзвешенном графе
(т.е. путь считается по количеству ребер, входящих в него)
'''
from collections import deque


def BFS_geodesic(graph, start_u, largest=False):
    """Поиск в ширину с подсчетом геодезического расстояния.
        Parameters
        ----------
        graph : Graph
            Граф
        start_u : int
            Стартовая вершина
        largest : bool
            Если True, то возвращает наибольшее расстояние от заданной вершины

    Возвращает:
        - эксцентриситет каждой вершины

    """
    dist = dict([(node, -1) for node in graph.nodes])
    dist[start_u] = 0
    available_nodes = deque()
    available_nodes.append(start_u)
    while available_nodes:
        current_node = available_nodes.popleft()
        for v in graph.adj_nodes(current_node):
            if dist[v] == -1:
                available_nodes.append(v)
                dist[v] = dist[current_node] + 1
    if largest:
        largest_distance_index = max(dist, key=lambda node: dist[node])
        return dist[largest_distance_index]
    return dist


class StateOfNode:
    # вершина и её предок
    # (для восстановления кратчайшего пути)
    def __init__(self, v, parent_state):
        self.node = v
        self.parent = parent_state


def BFS_search(graph, start_u, finish_v, length=False):
    # поиск кратчайшего (по числу ребер) пути между двумя вершинами
    if start_u == finish_v:
        return 0
    available_nodes = deque()
    start_state = StateOfNode(start_u, None)

    available_nodes.append(start_state)
    visited = {start_u}

    while available_nodes:
        current_state = (available_nodes.popleft())
        current_node = current_state.node
        for v in graph.adj_nodes(current_node):
            if v == finish_v:
                # восстанавливаем путь
                path = [finish_v, current_node]
                parent_state = current_state.parent
                while parent_state:
                    path.append(parent_state.node)
                    parent_state = parent_state.parent
                if length:
                    return len(path)-1
                return list(reversed(path))
            if v not in visited:
                visited.add(v)
                new_state = StateOfNode(v, current_state)
                available_nodes.append(new_state)
    # если пути не обнаружено
    return None


