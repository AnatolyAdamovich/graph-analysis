"""
Landmark-based
"""
from .BFS import *


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


def best_coverage_sample(graph, d):
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


