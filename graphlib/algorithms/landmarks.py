from .BFS import *


def approx_distance(dict_landmarks, s, t):
    """Приближенное расстояние между вершинами s и t с помощью Landmarks-алгоритмов

        Parameters:
        ----------
            dict_landmarks : dictionary
                словарь словариков, в котором для каждого выбранного по некоторому правилу
                ландмарка, вычислено расстояние до всех достижимых из него вершин
            s : any
                вершина, от которой ищем расстояние
            t : any
                вершина, до которой ищем расстояние

        Returns:
        ----------
            d: int
                аппроксимированное расстояние от s до t

        Examples:
        ----------
            approx_distance(dict_of_landmarks, 'A', 'B') = 12

        Notes:
        ----------
            Для нахождения реального расстояния можно использовать функцию BFS_search(graph, start_u, finish_v)
    """
    d = 1e7
    for u in dict_landmarks:
        if (s not in dict_landmarks[u]) or (t not in dict_landmarks[u]):
            # нет пути от s (или t) до ландмарка u
            continue
        temp_d = dict_landmarks[u][s] + dict_landmarks[u][t]
        if temp_d < d:
            d = temp_d
    return d


# --------------------MAIN ALGORITHMS-------------------
def landmark_basic(graph, number_of_landmarks, method='random', M=None):
    """Базовый алгоритм для построения embedding
        (вектора расстояний от вершины до каждого из Ландмарков)

        Parameters:
        ----------
            graph : graphlib.structures.Graph
                неориентированный граф
            number_of_landmarks : int
                число Ландмарков
            method : ['random', 'coverage', 'degree', 'centrality']
                стратегия выбора Ландмарков
            M: int
                для стратегии отбора 'coverage' требуется задавать число пар M
                (обязательный аргумент только при method=='coverage')

        Returns:
        ----------
            distance_to_landmarks: dict
                словарь словариков, в котором для каждого ландмарка вычислено расстояние
                до всех достижимых из него вершин (embedding)

        Examples:
        ----------
            landmark_basic(G, 2, method='random') = {'A':{'C':3, ..., 'D': 4},
            'B': {'C': 1, ... 'D':2}}

        Notes:
        ----------
            Более подробно о Landmark алгоритмах можно почитать в:
                1. Tretyakov, K., Armas-Cervantes, A., García-Bañuelos, L., Vilo, J. & Dumas, M. Fast fully
                dynamic landmark-based estimation of shortest path distances in very large graphs. Proc
                20th Acm Int Conf Information Knowl Management - Cikm ’11 1785–1794 (2011)
                doi:10.1145/2063576.2063834.

                2. Potamias, M., Bonchi, F., Castillo, C. & Gionis, A. Fast shortest path distance estimation in
                large networks. Proceeding 18th Acm Conf Information Knowl Management - Cikm ’09 867–
                876 (2009) doi:10.1145/1645953.1646063.
    """
    distance_to_landmarks = dict()

    if method == 'random':
        landmarks = random_sample(graph, d=number_of_landmarks)
    elif method == 'degree':
        landmarks = largest_degree_sample(graph, d=number_of_landmarks)
    elif method == 'coverage':
        landmarks = best_coverage_sample(graph, d=number_of_landmarks, M=M)
    elif method == 'centrality':
        landmarks = lowest_centrality_sample(graph, d=number_of_landmarks)
    else:
        # error
        return None
    for lm in landmarks:
        # геодезическое расстояние от Ландмарка до всех достижимых из нее
        # в виде словаря
        dist_from_lm_to_over = BFS_geodesic(graph, start_u=lm)
        distance_to_landmarks[lm] = dist_from_lm_to_over
    return distance_to_landmarks


def landmark_lca(graph):
    return 0


# -------------SAMPLING STRATEGIES----------------------
def random_sample(graph, d):
    """Случайный отбор ландмарков

        Parameters:
        ----------
            graph : graphlib.structures.Graph
                неориентированный граф
            d : int
                число Ландмарков

        Returns:
        ----------
            landmarks : list
                список отобранных вершин

        Examples:
        ----------
            random_sample(G, 50) = ['A1', 'A2', ..., 'A50']

        Notes:
        ----------
            Принято считать это самым простым способом отбора ландмарков
    """
    landmarks = graph.selection(d)
    return landmarks


def largest_degree_sample(graph, d):
    """Отбор ландмарков с наибольшим количеством соседей (смежных вершин)

        Parameters:
        ----------
            graph : graphlib.structures.Graph
                неориентированный граф
            d : int
                число Ландмарков

        Returns:
        ----------
            landmarks : list
                список отобранных вершин

        Examples:
        ----------
            largest_degree_sample(G, 50) = ['A1', 'A2', ..., 'A50']

        Notes:
        ----------
            Данный способ основан на идеи о том, что раз у вершины много соседей,
            то это значит, что она где-то в плотной части графа,
            а значит покрывает много кратчайших путей
    """
    landmarks = graph.selection(d, most_degree=True)
    return landmarks


def best_coverage_sample(graph, d, M):
    """Отбор ландмарков с наилучшим покрытием

        Parameters:
        ----------
            graph : graphlib.structures.Graph
                неориентированный граф
            d : int
                число Ландмарков
            M : int
                число пар, на основе которых производится оценка покрытия

        Returns:
        ----------
            landmarks : list
                список отобранных вершин

        Examples:
        ----------
            best_coverage_sample(G, 50, 100) = ['A1', 'A2', ..., 'A50']

        Notes:
        ----------
            Продвинутый способ отбора ландмарков. Подразумевает выбор M пар вершин случайным образом, нахождение
            кратчайших расстояний между ними, затем отбор Ландмарков, покрывающих максимальное число путей
            среди найденных
    """

    landmarks = []
    vertices_first = graph.selection(M)
    vertices_second = graph.selection(M)
    pairs = [(u, v) for u, v in zip(vertices_first, vertices_second)]
    nodes_coverage_paths = dict()  # словарик, в котором для каждой вершины
                                   # будут храниться индексы кратчайших путей, в которые она входит

    all_paths = set([i for i in range(M)])  # номера кратчайших путей
                                            # (чтобы не хранить все пути, будем хранить их номера)

    for index_of_path, (u, v) in enumerate(pairs):
        shortest_path = BFS_search(graph, start_u=u, finish_v=v)
        if shortest_path is None or len(shortest_path) == 0:
            continue
        for node in shortest_path[1:-1]:
            if node in nodes_coverage_paths:
                nodes_coverage_paths[node].add(index_of_path)  # добавляем номер пути
            else:
                nodes_coverage_paths[node] = {index_of_path}
    if len(nodes_coverage_paths) < d:
        print('Число вершин, покрываемых выбранными M путями, меньше числа выбираемых ландмарков d.'
              ' Необходимо задать большее число пар M или меньшее число ландмарков d')
        return None
    j = 0
    while j < d and len(all_paths) > 0:
        j += 1
        # выбираем вершину, покрывающую наибольшее число путей
        vertex = max(nodes_coverage_paths, key=lambda elem: len(all_paths & nodes_coverage_paths[elem]))
        all_paths = all_paths - nodes_coverage_paths[vertex]
        del nodes_coverage_paths[vertex] # удаляем данную вершину из словаря
        landmarks.append(vertex)
    if j == d:
        return landmarks
    else:
        rest = d - j
        for i in range(rest):
            vertex = max(nodes_coverage_paths, key=lambda elem: len(nodes_coverage_paths[elem]))
            del nodes_coverage_paths[vertex]  # удаляем данную вершину из словаря
            landmarks.append(vertex)
        return landmarks


def lowest_centrality_sample(graph, d):
    """Отбор ландмарков с наименьшей величиной the closest centrality

        Parameters:
        ----------
            graph : graphlib.structures.Graph
                неориентированный граф
            d : int
                число Ландмарков

        Returns:
        ----------
            landmarks : list
                список отобранных вершин

        Examples:
        ----------
            lowest_centrality_sample(G, 50) = ['A1', 'A2', ..., 'A50']

        Notes:
        ----------
            Способ, использующий метрику центральности.
            Вычисления проводятся дольше, но в некоторых случаях этот метод может быть лучшим
    """

    closeness_centrality = dict()
    n = graph.nodes_count
    for node in graph.nodes:
        distances = BFS_geodesic(graph, node)
        geo = sum(distances.values())
        if geo > 0:
            closeness_centrality[node] = n/geo
    cs_list = sorted(closeness_centrality.items(), key=lambda elem: elem[1])
    cs_list = cs_list[:d]
    landmarks = list(map(lambda elem: elem[0], cs_list))
    return landmarks


