import numpy as np
from math import radians
from params import ground_speed, k_wind


def get_bearing_to(node1, node2):
    """Computes bearing between two nodes."""
    dLon = (node2.latlonrad[1] - node1.latlonrad[1])
    x = np.cos((node2.latlonrad[0])) * np.sin((dLon))
    y = np.cos((node1.latlonrad[0])) * np.sin((node2.latlonrad[0])) - np.sin(
        (node1.latlonrad[0])) * np.cos((node2.latlonrad[0])) * np.cos((dLon))
    brngrad = np.arctan2(x, y)
    brng = np.degrees(brngrad)

    return brng

def get_wind_to(node1, node2):
    """Computes wind between two nodes."""
    brngrad = radians(node1.get_bearing_to(node2))

    uwind = (node1.uwind + node2.uwind) / 2
    vwind = (node1.vwind + node2.vwind) / 2

    # tailwind = uwind * np.cos(brngrad) + vwind * np.sin(brngrad)
    # crosswind = -uwind * np.sin(brngrad) + vwind * np.cos(brngrad)
    tailwind = uwind * np.cos(brngrad) - vwind * np.sin(brngrad)
    crosswind = uwind * np.sin(brngrad) + vwind * np.cos(brngrad)
    return tailwind, crosswind

def get_thrust_to(node1, node2, ground_speed, wind):
    """Computes thrust between two nodes."""
    tailwind, crosswind = 0, 0
    if wind == "wind":
        tailwind, crosswind = get_wind_to(node1, node2)
    return (ground_speed + k_wind*tailwind)**2 + k_wind*crosswind**2

def get_fuel_cost(node1, node2, wind):
    """Computes fuel-cost between two nodes."""
    thrust = get_thrust_to(node1, node2, ground_speed, wind)
    fuel = thrust * node1.get_distance_to(node2)
    
    return fuel

def get_dop_cost(dop1, dop2):
    dop_cost = dop1 + dop2
    return dop_cost

def get_kinematic_cost(node1, node2):
    yaw = (np.abs(node1.latlon[0]-node2.latlon[0]))/(np.abs(node1.latlon[1]-node2.latlon[1]))
    pitch = np.abs(node1.latlon[2]-node2.latlon[2])
    return yaw + pitch

def get_optim_cost(dop1, dop2, node1, node2, wind):
    optim_cost = (get_fuel_cost(node1, node2, wind)) * get_dop_cost(dop1, dop2) #+  get_kinematics_to(node1,node2)
    return optim_cost