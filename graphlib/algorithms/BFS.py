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

    Функция возвращает словарь, в котором для каждой вершины
     указано геодезическое расстояние
        """
    dist = dict([(node, -1) for node in graph.nodes])
    dist[start_u] = 0
    available_nodes = deque()
    available_nodes.append(start_u)
    while available_nodes:
        current_node = available_nodes.popleft()
        for v in graph.neighbors_for_node(current_node):
            if dist[v] == -1:
                available_nodes.append(v)
                dist[v] = dist[current_node] + 1
    if largest:
        largest_distance_index = max(dist, key=lambda node: dist[node])
        return dist[largest_distance_index]
    return dist



def BFS_with_search(graph, start_u, finish_v):
    # поиск кратчайшего пути (по числу ребер) между двумя вершинами
    available_nodes = deque()
    visited = set()


