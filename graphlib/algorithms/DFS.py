from collections import deque


def DFS_with_cc(graph, largest=False):
    """Поиск в глубину для нахождения компонент связности.

        Parameters:
        ----------
            graph : graphlib.structure.Graph
                неориентированный граф
            largest : bool
                если True, то ко всему прочему возвращает номер наибольшей компоненты

        Returns:
        ----------
            cc_num: int
                число компонент связности
            max_component_number: int
                номер наибольшей компоненты (если largest==True)
            cc: dict
                словарь, содержащий компоненты связности (каждая компонента характеризуется своим номером)


        Examples:
        ----------
            DFS_with_cc(G) = 2,  {1: ['A', 'E', 'C', 'D'], 2: ['T', 'Y', 'R']}

            DFS_with_cc(G, largest=True) = 2, 1, {1: ['A','E', 'C', 'D'], 2: ['T', 'Y', 'R']}
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
    """Рекурсивная реализация DFS. Подходит для графов небольшой размерности из-за ограничения
        в использовании рекурсии.

        Parameters:
        ----------
                graph : graphlib.structure.Graph
                    неориентированный граф

        Returns:
        ----------
                time_in: dict
                    время входа в каждую вершину при обходе DFS
                time_out: dict
                    время выхода из каждой вершины при обходе DFS

        Examples:
        ----------
                DFS_with_times_recursive(G) = {'A': 1, 'B': 2, 'C': 3}, {'A': 6, 'B': 5, 'C': 4}

        Notes:
        ----------
            Может быть использована для алгоритма Косарайю, когда требуется знать время входа
            и выхода из вершины при обходе графа.
    """

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
