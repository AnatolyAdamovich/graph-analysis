''' Поиск компонент слабой и сильной связности в графах '''
from collections import deque
from .DFS import *


def weakly_components(digraph, largest=False):
    graph = digraph.to_simple()
    return DFS_with_cc(graph, largest)


def strongly_components(digraph,):
    pass
