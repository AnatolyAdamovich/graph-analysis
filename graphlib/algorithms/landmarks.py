"""
Landmark-based
"""
from .BFS import *
from random import sample


# --------------------DISTANCE--------------------------
def approx_distance(dict_landmarks, s, t):
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
def landmark_basic(graph, number_of_landmarks, method='random'):
    """
    basic landmark algorithm
    Parameters:
    -----------------
        graph: Graph
        number_of_landmarks: int
        method: ['random', 'degree', 'coverage', 'centrality']
    """
    distance_to_landmarks = dict()

    if method == 'random':
        landmarks = random_sample(graph, d=number_of_landmarks)
    elif method == 'degree':
        landmarks = largest_degree_sample(graph, d=number_of_landmarks)
    elif method == 'coverage':
        landmarks = best_coverage_sample(graph, d=number_of_landmarks)
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
    landmarks = graph.selection(d)
    return landmarks


def largest_degree_sample(graph, d):
    landmarks = graph.selection(d, most_degree=True)
    return landmarks


def best_coverage_sample(graph, d, M):
    # d - число ландмарков
    # M - число ребер для выбора Ландмарков
    landmarks = []
    edges_sample = sample(graph.edges_list(), k=M)
    nodes_coverage_paths = dict()  # словарик, в котором для каждой вершины
                                   # будут храниться индексы кратчайших путей, в которые она входит

    all_paths = set([i for i in range(M)])  # номера кратчайших путей
                                            # (чтобы не хранить все пути, будем хранить их номера)

    for index_of_path, (u, v) in enumerate(edges_sample):
        shortest_path = BFS_search(graph, start_u=u, finish_v=v)

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






    return 0


def lowest_centrality_sample(graph, d):
    closeness_centrality = dict()
    n = graph.nodes_count
    for node in graph.nodes:
        distances = BFS_geodesic(graph, node)
        geo = sum(distances.values())
        if geo > 0:
            closeness_centrality[node] = n/geo
    cs_list = sorted(closeness_centrality.items(), key=lambda elem: elem[1])
    cs_list = cs_list[:d]
    cs_list = list(map(lambda elem: elem[0], cs_list))
    return cs_list


