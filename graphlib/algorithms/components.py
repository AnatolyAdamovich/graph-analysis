''' Поиск компонент слабой и сильной связности в графах '''
from .DFS import *
from ..structures.digraph import Digraph


def weakly_components(digraph, largest=False):
    """Поиск компонент слабой связности

        Parameters:
        ----------
            digraph : graphlib.structure.DiGraph
                ориентированный граф

            largest : bool
                если True, то возвращает номер наибольше компоненты

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
            weakly_components(DG) = 2,  {1: ['A', 'E', 'C', 'D'], 2: ['T', 'Y', 'R']}

            weakly_components(DG, largest=True) = 2, 1, {1: ['A','E', 'C', 'D'], 2: ['T', 'Y', 'R']}
    """
    graph = digraph.to_simple()
    return DFS_with_cc(graph, largest)


def strongly_components_tarjan(digraph):
    """Поиск компонент сильной связности с помощью алгоритма Тарьяна,
        который использует всего один проход в глубину и не требует рекурсии

        Parameters:
        ----------
            digraph : graphlib.structure.DiGraph
                ориентированный граф

        Returns:
        ----------
            итератор на список сильно связных компонент

        Examples:
        ----------
            list(strongly_components_tarjan(DG)) = [{'A', 'B', 'C'}, {'T', 'E}]

            or

            for scc in strongly_components_tarjan(DG): do something
    """

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


def strongly_components_kosaraju(digraph):
    """Поиск компонент сильной связности с помощью алгоритма Косарайю,
        который использует всего два обхода в глубину и требует рекурсии,
        поэтому не подходит для графов большой размерности

        Parameters:
        ----------
            digraph : graphlib.structure.DiGraph
                ориентированный граф

        Returns:
        ----------
            scc: dictionary
                словарь с компонентами сильной связности, где каждая компонента помечена номером

        Examples:
        ----------
            strongly_components_kosaraju(DG) = {1: ['A', 'T', 'E'],  2: ['B', 'R']}

    """

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


def meta_graph(digraph, scc=None):
    """Построение мета-графа для исходного орграфа

        Parameters:
        ----------
            digraph : graphlib.structure.DiGraph
                ориентированный граф
            scc : list
                список компонент сильной связности (необязательный)

        Returns:
        ----------
            condensation : graphlib.structure.DiGraph
                конденсация исходного орграфа

        Notes:
        ----------
            Мета-графа представляет собой граф, в котором вершинами являются компоненты сильной связности.
            Ребра показывают связь разных компонент. Вершины представлены номерами (индексами соответствующих компонент).
            Каждая вершина в мета-графе также хранит информацию о том, какие вершины исходного графа ей принадлежат
            (в аттрибуте digraph.information).

    """

    # scc - компоненты сильной связности в виде списка кортежей
    if scc is None:
         scc = list(strongly_components_tarjan(digraph))

    # вершины в метаграфе будут представлять собой множества вершин исходного digraph
    nodes_in_meta = dict()
    nodes_label = dict()
    for index, component in enumerate(scc):
        nodes_in_meta[index] = component
        for v in component:
            nodes_label[v] = index
    edges_in_digraph = digraph.edges_list()
    edges_in_meta = [(nodes_label[u], nodes_label[v]) for (u, v) in edges_in_digraph
                     if nodes_label[u] != nodes_label[v]]
    condensation = Digraph(name='meta-graph::' + digraph.name,
                           nodes=nodes_in_meta,
                           edges=edges_in_meta)
    return condensation
