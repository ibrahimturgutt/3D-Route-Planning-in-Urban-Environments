import startup as su
import astar
import time
import utils
from params import filename, k_neighbours, start_latlon, end_latlon, heuristic, method, cpath_modu, start, end, dop
path = []


t0, t_startup, t_astar, t_cpath = None, None, None, None


def initialisation(h):
    """Loads the grb2 file."""
    print("\n---------------------\n")
    global t0
    global t_startup
    global df
    t0 = time.time()

    print("Startup... " + str(k_neighbours) + " neighbours; method: " +
          method + "; heuristic: " + h)

    nodes = su.startup(filename, k_neighbours, method, h, dop)

    start_id = su.find_closest(nodes, start_latlon[0:2])
    end_id = su.find_closest(nodes, end_latlon[0:2])

    t_startup = time.time()

    print("Start: " + str(nodes[start_id]))
    print("End: " + str(nodes[end_id]))
    print("Startup: " + str(t_startup - t0) + " s\n")
    return start_id, end_id, nodes


def astar_call(start_id, end_id, nodes, h):
    """Calls the astar function with appropriate parameters."""
    global t_astar
    global t_startup
    global t0
    print("Astar...")
    path, explored = astar.astar(nodes, start_id, end_id, k_neighbours,
                                  method, h, dop)
    t_astar = time.time()
    print("Astar: " + str(t_astar - t_startup) + " s")
    print("Total: " + str(t_astar - t0) + " s")

    return path, explored


def closest(path, nodes):
    """Calls function to find the closest path to the great-circle path using the grid of the grb2 files."""
    global t_astar
    global t_cpath
    print("\n")
    print("Closest path...")

    s = path[0]
    e = path[-1]

    cpath = utils.closest_path(s, e, nodes, cpath_modu)
    t_cpath = time.time()

    print("Closest path: " + str(t_cpath - t_astar) + " s")

    return cpath


def compare(cpath):
    """Compare distance between two paths and the great-circle path."""
    s = path[0]
    e = path[-1]
    astar_len = utils.path_len(path)
    cpath_len = utils.path_len(cpath)
    great_circle_len = s.get_distance_to(e)

    print("\n")
    print("A--star path len: " + str(astar_len/1000) + " m")
    print("Closest path len: " + str(cpath_len/1000) + " m")
    print("Great circle len: " + str(great_circle_len/1000) + " m")


def plot(path, cpath, filename):
    """Plots the paths."""
    utils.plot_path(path, cpath, filename)


start_id, end_id, nodes = initialisation(heuristic)
path, explored = astar_call(start_id, end_id, nodes, heuristic)


cost_optim = utils.path_optim_cost(path, dop)

filename_tmp = start + " to " + end
filename_out = "fig/"

for i in range(len(filename_tmp)):
    c = filename_tmp[i]
    if filename_tmp[i] == " ":
        c = "_"
    filename_out += c



plot(path, path, filename_out)

print("\n")



utils.reinit(nodes)
start_id, end_id, nodes = initialisation("distance")
path2, explored = astar_call(start_id, end_id, nodes, "distance")
cost_shortest = utils.path_optim_cost(path2, dop)


    
dop_path = []
for i in range(len(path)):
    path_dop = path[i].latlon[-1]
    dop_path.append(path_dop)
    





print("\n\n")
print("Cost with optimised path: " + str(cost_optim))
print("Cost with shortest path: " + str(cost_shortest))
print("Ratio: " + str(cost_shortest/cost_optim))
print("\n\n")
print("Path with DoP Coefficient: ")
print(str(path))
print("Average DoP Coefficient of the Path: " + str(sum(dop_path)/len(dop_path)))

# print(str(path2))
# print("Average DoP Coefficient of the Path: " + str(sum(dop_path2)/len(dop_path2)))