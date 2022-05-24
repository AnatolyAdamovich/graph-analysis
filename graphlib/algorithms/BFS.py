from collections import deque


def BFS_geodesic(graph, start_u, largest=False):
    """Поиск в ширину с подсчетом геодезического расстояния.

    Parameters:
    ----------
        graph : graphlib.structure.Graph
            неориентированный граф
        start_u : any
            стартовая вершина,от которой будет считаться расстояние до других вершин.
        largest : bool
            если True, то возвращает наибольшее расстояние от start_u до некоторой достижимой вершины (эксцентриситет вершины)

    Returns:
    ----------
        dist: dictionary
            словарь, содержащий геодезическое расстояние от start_u до всех достижимых из нее вершин
        largest_distance: int
            эксцентриситет вершины (в случае largest==true)
    Examples:
    ----------
        BFS_geodesic(G, 'A') = {'B': 2, 'C': 3}

        BFS_geodesic(G, 'A', largest=True) = 3
    """
    dist = dict()
    dist[start_u] = 0
    available_nodes = deque()
    available_nodes.append(start_u)
    while available_nodes:
        current_node = available_nodes.popleft()
        for v in graph.adj_nodes(current_node):
            if v not in dist:
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
    """Поиск в ширину для нахождения кратчайшего геодезического расстояния между двумя вершинами.

        Parameters:
        ----------
            graph : graphlib.structure.Graph
                неориентированный граф
            start_u : any
                стартовая вершина
            finish_v : any
                конечная вершина
            length : bool
                если True, то возвращает геодезического расстояние между вершинами

        Returns:
        ----------
            path: list
                путь от start_u до finish_v в виде списка вершин; если пути не обнаружено, то None

        Examples:
        ----------
            BFS_search(G, 'A', 'B') = ['A', 'C', 'D', 'B']

            BFS_search(G, 'A', 'B', length=True) = 3
        """
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


def BFS_with_SPT(graph, root_vertex):
    """Поиск в ширину для нахождения дерева кратчайших путей с корневой вершиной root_vertex

        Parameters:
        ----------
            graph : graphlib.structure.Graph
                неориентированный граф
            root_vertex : any
                вершина, от которой будет строиться дерево (корневая)

        Returns:
        ----------
            spt : dict
                дерево кратчайших путей в виде словаря

        Examples:
        ----------
            BFS_with_SPT(G, 'A') = {'B': StateOfNode(), 'C': StateOfNode(), ...}

        Notes:
        ----------
            Для хранения дерева используются структуры, хранящие ссылки на родительские узлы.
            Например, если при обходе BFS сначала был осуществлен спуск в вершину 'B',
            а затем в вершину 'C', то StateOfNode() для 'B' будет хранить вершину 'C'
            в качестве родительского узла.
            Это позволит восстановить путь от любой (достигнутой) вершины до корня.
        """
    spt = dict()
    available_nodes = deque()
    start_state = StateOfNode(root_vertex, None)

    available_nodes.append(start_state)
    visited = {root_vertex}

    while available_nodes:
        current_state = (available_nodes.popleft())
        current_node = current_state.node
        for v in graph.adj_nodes(current_node):
            if v not in visited:
                visited.add(v)
                new_state = StateOfNode(v, current_state)
                spt[v] = new_state
                available_nodes.append(new_state)

    return spt

