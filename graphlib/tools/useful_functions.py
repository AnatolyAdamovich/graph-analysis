'''Функции для анализа графов и др.'''
from ..algorithms import BFS_geodesic, BFS_search, select_landmarks,\
    landmark_basic, landmark_lca, approx_distance_basic, approx_distance_lca
from time import time

def density(graph):
    """Плотность графа

        Parameters:
        ----------
            graph : graphlib.structures.Graph or DiGraph
                граф

        Returns:
        ----------
            density: float
                плотность исходного графа
        Examples:
        ----------
            density(G) = 0.445

        Notes:
        ----------
            Плотность графа - это отношения числа его вершин к числу ребер в полном графе на том же числе вершин

            Число ребер в полном графе вычисляется по формуле ( n * (n-1) ) / 2, где n - число вершин
    """
    v = graph.nodes_count
    k_graph_edges = 0.5 * v * (v - 1)
    return graph.edges_count / k_graph_edges


def diameter(graph, with_node=False):
    """Диаметр графа

        Parameters:
        ----------
            graph : graphlib.structures.Graph or DiGraph
                граф
            with_node : bool
                если True, то возвращает вершины, между которыми был найден диаметр

        Returns:
        ----------
            d: int
                диаметр графа
            node1, node2: any
                вершины, между которыми найдено наибольшее геодезического расстояние (при with_node==True)
        Examples:
        ----------
            diameter(G) = 13

            diameter(G, with_node=True) = 13, 'A', 'B'

        Notes:
        ----------
            Диаметр графа - это наибольший из эксцентриситетов его вершин
            (наибольшее из максимальных кратчайших расстояний
            между парой вершин в графе)
    """
    d = -1
    node1 = -1
    node2 = -1
    for u in graph.nodes:
        current_geo = BFS_geodesic(graph, u)
        v = max(current_geo, key=lambda vertex: current_geo[vertex])
        if current_geo[v] > d:
            node1 = u
            node2 = v
            d = current_geo[v]
    if with_node:
        return d, node1, node2
    return d


def radius(graph, with_central=False):
    """Диаметр графа

        Parameters:
        ----------
            graph : graphlib.structures.Graph or DiGraph
                граф
            with_central : bool
                если True, то возвращает центральную вершину графа

        Returns:
        ----------
            r: int
                радиус графа
            node: any
                центральная вершина (при with_central == True)
        Examples:
        ----------
            radius(G) = 5

            radius(G, with_central=True) = 5, 'A'

        Notes:
        ----------
            Радиус графа - это наименьший из эксцентриситетов его вершин
            Минимальное среди максимальных кратчайших расстояний между вершиной
            до всех остальных в графе
    """
    r = 1e+10
    node = -1
    for u in graph.nodes:
        current_geo = BFS_geodesic(graph, u, largest=True)
        if current_geo < r:
            node = u
            r = current_geo
    if with_central:
        return r, node
    return r


# оценка
def approximate_statistic(graph, number=500, percent=90, nodes=None):
    """ Приближенные статистики графа по выборке фиксированного размера

        Parameters:
        ----------
            graph : graphlib.structures.Graph or DiGraph
                граф
            number : int
                число вершин для выборки (default = 500)
            percent : int
                доля квартиля (default = 90)
            nodes : list
                если выборка уже есть, то можно считать характеристики на ее основе (default=None)
        Returns:
        ----------
            approx_diam: int
                приближенный диаметр
            approx_radius: int
                приближенный радиус
            approx_percentile: int
                приближенный квартиль
        Examples:
        ----------
            approx_statistics(G) = 13, 5, 4

        Notes:
        ----------
            Радиус графа - это наименьший из эксцентриситетов его вершин
            Минимальное среди максимальных кратчайших расстояний между вершиной
            до всех остальных в графе;

            Диаметр графа - это наибольший из эксцентриситетов его вершин
            (наибольшее из максимальных кратчайших расстояний
            между парой вершин в графе);

            Квартиль расстояния - это геодезическое расстояние,
            которое встречается чаще определенного процента
            других возможных геодезических расстояний в графе.
    """
    if nodes is None:
        nodes = list(graph.selection(x=number))
    d = 0
    r = 1e+10
    list_with_eccentricities = []
    distances = []
    for vertex in nodes:
        current_geo = BFS_geodesic(graph, vertex)
        distances += list(current_geo.values())
        list_with_eccentricities.append(max(current_geo.values()))
    # for i in range(len(nodes)-1):
    #     u = nodes[i]
    #     for j in range(i+1, len(nodes)):
    #         v = nodes[j]
    #         current_distance = BFS_search(graph, u, v, length=True)
    #         if current_distance > d:
    #             d = current_distance
    #             node1, node2 = u, v

    approx_radius = min(list_with_eccentricities)
    approx_diameter = max(list_with_eccentricities)

    distances.sort()
    n = len(distances)
    approx_percentile = distances[round(n * (percent / 100)) - 1]

    return approx_diameter, approx_radius, approx_percentile


def number_of_triangles(graph):
    """Число треугольников в графе (полных графов на 3 вершинах)

        Parameters:
        ----------
            graph : graphlib.structures.Graph
                неориентированный граф

        Returns:
        ----------
            number : int
                число треугольников в graph

        Examples:
        ----------
            number_of_triangles(G) = 331

        Notes:
        ----------
            перебираются все ребра (u,v) графа

            для всех соседей вершины u проверяется:

            сосед смежен с вершиной v?

            если да, то это очередной треугольник

            разделить число найденных треугольников на 3
    """
    count = 0
    all_edges = iter(graph.edges_list())
    for (u, v) in all_edges:
        if u != v:
            for w in graph.neighbors_for_node(u):
                if w != u and w != v:
                    if graph.adj_nodes_checking(w, v):
                        count += 1
    return int(count / 3)


def local_clustering_coefficient(graph, vertex):
    """Локальный кластерный коэффициент

        Parameters:
        ----------
            graph : graphlib.structures.Graph
                неориентированный граф
            vertex : any
                вершина, для которой требуется посчитать коэффициент

        Returns:
        ----------
            coef : float
                локальный кластерный коэффициент

        Examples:
        ----------
            local_clustering_coefficient(G, 'A') = 0.4

        Notes:
        ----------
            Локальный кластерный коэффициент показывает вероятность того,
            что две смежные к данной вершины тоже будут являться смежными
    """
    neighbors = graph.adj_nodes(vertex)
    deg = len(neighbors)
    if deg < 2:
        return 0
    edges_number = 0
    if vertex in neighbors:
        neighbors.remove(vertex)
    for v in neighbors:
        for w in neighbors:
            if w != v and graph.adj_nodes_checking(v, w):
                edges_number += 1
    return edges_number/(deg*(deg-1))


def average_clustering_coefficient(graph):
    """Средний кластерный коэффициент графа

        Parameters:
        ----------
            graph : graphlib.structures.Graph
                неориентированный граф

        Returns:
        ----------
            coef : float
                средний кластерный коэффициент

        Examples:
        ----------
            average_clustering_coefficient(G) = 0.63

        Notes:
        ----------
            Представляет собой оценку глобального кластерного коэффициента
            и вычисляется как усредненная сумма локальных кластерных коэффициентов
    """
    result = 0
    for u in graph.nodes:
        result += local_clustering_coefficient(graph, u)
    return result / graph.nodes_count


def global_clustering_coefficient(graph):
    """Глобальный кластерный коэффициент графа

        Parameters:
        ----------
            graph : graphlib.structures.Graph
                неориентированный граф

        Returns:
        ----------
            coef : float
                глобальный кластерный коэффициент

        Examples:
        ----------
            global_clustering_coefficient(G) = 0.63

        Notes:
        ----------
            https://en.wikipedia.org/wiki/Clustering_coefficient
    """
    numerator, denominator = 0, 0
    # n * (n-1) * (1/2) - number of triplets for node
    # where n = number of neighbors
    for vertex in graph.nodes:
        local_cluster = local_clustering_coefficient(graph, vertex)
        deg = len(graph.adj_nodes(vertex))
        if deg >= 2:
            binomial_coeff = deg * (deg-1) / 2
            numerator += (local_cluster * binomial_coeff)
            denominator += binomial_coeff

    return numerator/denominator


def make_data_pairs(graph, number_of_pairs):
    """Функция для создания заданного числа пар вершин с подсчитанным
        геодезическим расстоянием между ними

        Parameters:
        ----------
            graph : graphlib.structures.Graph
                неориентированный граф
            number_of_pairs : graphlib.structures.Graph
                количество пар

        Returns:
        ----------
            data : list
                список кортежей вида: (вершина1, вершина2, расстояние между ними)

        Examples:
        ----------
            make_data(G, 3) = [('A', 'B', 3), ('T', 'K', 10), ('U', 'L', 5)]

    """
    i = 0
    data = []
    while i < number_of_pairs:
        node1, node2 = list(graph.selection(2))
        dist = BFS_search(graph, node1, node2, length=True)
        if dist is not None:
            data.append((node1, node2, dist))
            i += 1
    return data


def experiment(graph, data_real_distances, algorithm, selection_strategy,
               N_of_landmarks, N_of_pairs_for_coverage=None, with_time=False):
    """Функция для проведения эксперимента и вычисления approximate error

        Parameters:
        ----------
            graph : graphlib.structures.Graph
                неориентированный граф
            data_real_distances : list
                список пар вершин с реально подсчитанным геодезическим расстоянием между ними
            algorithm : ['basic', 'LCA']
                алгоритм оценивания; см. функции alg.landmark_basic, alg.landmark_lca
            selection_strategy : ['random', 'centrality', 'coverage', 'degree']
                алгоритм отбора ландмарков; см. функцию alg.select_landmarks
            N_of_landmarks : int
                количество ландмарков для отбора
            N_of_pairs_for_coverage : int
                количество пар для best_coverage_sampling
            with_time : bool
                если True, то будет возвращен словарик, содержащий время работы каждого этапа

        Returns:
        ----------
            approx_error : float
                ошибку приближения при заданных параметрах
            dict_with_time: dictionary
                время работы каждого этапа алгоритма (возвращается, если with_time==True)

        Examples:
        ----------
            experiment(G, data, 'basic', 'degree', 100) = 0.25

    """

    landmarks = select_landmarks(graph, method=selection_strategy,
                                 number_of_landmarks=N_of_landmarks,
                                 number_of_pairs=N_of_pairs_for_coverage)
    approx_error = 0
    if with_time:
        dict_with_time = dict()
        if algorithm == 'basic':
            t_start = time()
            embedding = landmark_basic(graph, landmarks)
            t_finish = time()
            dict_with_time['building'] = t_finish-t_start

            t_start = time()
            for s, t, real_d in data_real_distances:
                estimate_of_distance = approx_distance_basic(embedding, s, t)
                approx_error += (estimate_of_distance - real_d) / real_d
            t_finish = time()

            approx_error /= len(data_real_distances)
            dict_with_time['estimation'] = t_finish-t_start
        elif algorithm == 'LCA':
            t_start = time()
            dictionary_with_spt = landmark_lca(graph, landmarks)
            t_finish = time()
            dict_with_time['building'] = t_finish - t_start

            t_start = time()
            for s, t, real_d in data_real_distances:
                estimate_of_distance = approx_distance_lca(dictionary_with_spt, s, t)
                approx_error += (estimate_of_distance - real_d) / real_d
            t_finish = time()

            approx_error /= len(data_real_distances)
            dict_with_time['estimation'] = t_finish - t_start
        return approx_error, dict_with_time
    else:
        if algorithm == 'basic':
            embedding = landmark_basic(graph, landmarks)
            for s, t, real_d in data_real_distances:
                estimate_of_distance = approx_distance_basic(embedding, s, t)
                approx_error += (estimate_of_distance-real_d)/real_d
            approx_error /= len(data_real_distances)
        elif algorithm == 'LCA':
            dictionary_with_spt = landmark_lca(graph, landmarks)
            for s, t, real_d in data_real_distances:
                estimate_of_distance = approx_distance_lca(dictionary_with_spt, s, t)
                approx_error += (estimate_of_distance-real_d)/real_d
            approx_error /= len(data_real_distances)
        return approx_error
