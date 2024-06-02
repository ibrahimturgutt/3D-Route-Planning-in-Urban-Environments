import numpy as np
from sklearn.neighbors import BallTree
import pygrib
import structure as st
from params import wgs84


def find_closest(nodes, latlon):
    """Find closest node to a latitude-longitude coordinate"""
    latlonrads = [node.latlonrad for node in nodes]
    # nbrs = NB(n_neighbors=2, algorithm='ball_tree').fit(latlonrads)
    # _, index = nbrs.kneighbors([np.deg2rad(latlon)])
    tree = BallTree(latlonrads, leaf_size=2, metric='haversine')
    _, index = tree.query([np.deg2rad(latlon)], k=1)
    return index[0][0]


def startup(filename, k_neighbours, method, heuristic, dop):
    """Loads grb2 file."""

    # Read in a file
    file = filename
    gr = pygrib.open(file)  # pylint: disable=maybe-no-member

    # Note that msg 328 is u direction of the wind and 329 is v directions.
    # Obtain these two messages.
    umsg = gr[328]
    vmsg = gr[329]

    # get the values into a matrix.
    uwind = umsg.values[190][43]
    vwind = vmsg.values[190][43]

    lats, lons, heights, dops = wgs84.iloc[:]['latitude'], wgs84.iloc[:
        ]['longitude'], wgs84.iloc[:]['height'], wgs84.iloc[:]['dop']

    d = {}
    nodes = []

    for i in range(lats.shape[0]):

        # for j in range(lats.shape[1]):

        latlon = (lats[i], lons[i], heights[i]+60, dops[i])

        nodes.append(st.Node(latlon, uwind, vwind, dop[i]))
        d[latlon] = nodes[-1]

    #nodes.sort(key=lambda x: x.latlon[0])  # sort by lat

    for i in range(len(nodes)):
        nodes[i].id = i

    if method == "old":  # old-method creates the graph on startup
        find_all_neighbours(nodes, k_neighbours, heuristic)

    return nodes


def find_all_neighbours(nodes, k_neighbours, heuristic, dop):
    """Creates the graph from the nodes list."""

    latlonrads = [node.latlonrad for node in nodes]

    tree = BallTree(latlonrads, metric='haversine')
    # find k closest neighbours for each point
    _, indices = tree.query(latlonrads, k=k_neighbours)

    indices = indices.tolist()

    for i in range(len(indices)):  # if a is b's neighbour then b is a's neighbour
        for index in indices[i]:
            if not (i in indices[index]):
                indices[index].append(i)
    for i in range(len(nodes)):
        nodes[i].id = i
        nodes[i].neighbours = []
        for j in indices[i]:
            if i != j:
                if heuristic == 'DoP':
                    if dop[nodes[i].id] <= 4.5:
                        weight= nodes[i].get_score_to(nodes[j], heuristic)
                        nodes[i].neighbours.append(
                            st.Neighbour(j, nodes[j], weight))
                else:
                    weight= nodes[i].get_score_to(nodes[j], heuristic)
                    nodes[i].neighbours.append(
                        st.Neighbour(j, nodes[j], weight))
