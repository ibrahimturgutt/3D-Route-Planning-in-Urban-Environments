from heapdict import heapdict
from sklearn.neighbors import BallTree

def find_path(node):
    """At the end of A-star, recreates path from the last node."""
    n = node
    path = []

    while n is not None:
        path.append(n)
        n = n.pred

    path.reverse()
    return path


def astar(g, start_id, end_id, k_neighbours, method, heuristic, dop):
    """A-star algorithm."""
    latlonrads = [node.latlonrad for node in g]

    tree = BallTree(latlonrads, metric='haversine')
    s = g[start_id]
    e = g[end_id]

    s.dist = 0
    hd = heapdict()
    hd[s] = s.dist
    explored = []

    s.gscore = 0
    s.fscore = s.get_score_to(g[end_id], heuristic)

    while hd:
        current = hd.popitem()[0]

        if current == e:
            current.get_neighbours(g, k_neighbours, tree, heuristic)
            return find_path(e), explored

        if method == "new" and not current.neighbours:
            current.get_neighbours(g, k_neighbours, tree, heuristic)

        for neighbour_N in current.neighbours:

            tentative_gscore = current.gscore + neighbour_N.weight
            neighbour = neighbour_N.node

            if neighbour.gscore > tentative_gscore:
                neighbour.pred = current
                neighbour.gscore = tentative_gscore
                neighbour.fscore = neighbour.gscore + \
                    neighbour.get_score_to(g[end_id], heuristic, "nowind")
                hd[neighbour] = neighbour.fscore
        explored.append(current)

    print('Not Found')
    return ('Not Found', 'Not Found')


