import numpy as np
from math import radians
from dataclasses import dataclass
import model

import structure as st


class Node():

    def __init__(self, latlon, dop, uwind, vwind):
        self.latlon = latlon
        self.latlonrad = [radians(latlon[0]), radians(latlon[1])]
        self.uwind = uwind
        self.vwind = vwind
        self.pred = None
        self.gscore = float('inf')
        self.fscore = float('inf')
        self.id = None
        self.neighbours = []
        self.itern = None
        self.dop = dop


    def __repr__(self):
        return "Node %6d, (%7.14f, %7.14f, %7.3f, %d)" % (self.id, self.latlon[0], self.latlon[1], self.latlon[2], self.latlon[3])

    def is_neighbour(self, other):
        c = False
        for neighbour in self.neighbours:
            if neighbour.id == other.id and neighbour.dop <= 4.5:
                if neighbour.dop <= 4.5:
                    c = True
                
        return c

    def get_bearing_to(self, other):
        """Returns bearing to another node."""
        dLon = (other.latlonrad[1] - self.latlonrad[1])
        x = np.cos((other.latlonrad[0])) * np.sin((dLon))
        y = np.cos((self.latlonrad[0])) * np.sin((other.latlonrad[0])) - np.sin(
            (self.latlonrad[0])) * np.cos((other.latlonrad[0])) * np.cos((dLon))
        brngrad = np.arctan2(x, y)
        brng = np.degrees(brngrad)

        return brng
    
    def get_wind_to(self, other):
        """Returns wind to another node. Wind is considered to be the average wind."""
        brngrad = radians(self.get_bearing_to(other))

        uwind = (self.uwind + other.uwind) / 2
        vwind = (self.vwind + other.vwind) / 2

        tailwind = uwind * np.cos(brngrad) + vwind * np.sin(brngrad)
        crosswind = -uwind * np.sin(brngrad) + vwind * np.cos(brngrad)

        return tailwind, crosswind
    
    def get_dop(self, other):
        dop_s = self.dop
        dop_o = other.dop
        return (dop_s + dop_o) / 2
    

    def get_distance_to(self, other):
        """Returns the distance to another node."""
        lat_s = self.latlon[0]
        lon_s = self.latlon[1]
        lat_o = other.latlon[0]
        lon_o = other.latlon[1]

        return np.sqrt((lat_s - lat_o)**2 + (lon_s - lon_o)**2) #111120 * np.rad2deg(np.arccos(np.sin(lat_s)*np.sin(lat_o) + np.cos(lat_s)*np.cos(lat_o)*np.cos(lon_o - lon_s)))

    def get_distance_to_gc(self, other):
        """Returns the distance to another node."""
        lat_s = self.latlonrad[0]
        lon_s = self.latlonrad[1]
        lat_o = other.latlonrad[0]
        lon_o = other.latlonrad[1]

        return 111120 * np.rad2deg(np.arccos(np.sin(lat_s)*np.sin(lat_o) + np.cos(lat_s)*np.cos(lat_o)*np.cos(lon_o - lon_s)))


    def get_kinematics_to(node1, node2):
        yaw = (np.abs(node1.latlon[0]-node2.latlon[0]))/(np.abs(node1.latlon[1]-node2.latlon[1]))
        pitch = np.abs(node1.latlon[2]-node2.latlon[2])
        return yaw + pitch 
    
 
    def get_score_to(self, other, heuristic, wind="wind"):
        """Returns the fuel cost or distance to another node depending on heuristic."""
        distance = self.get_distance_to(other)
        if heuristic == "distance":
            return distance
        else:
            return model.get_fuel_cost(self, other, wind) + model.get_kinematic_cost(self, other)
        
    
    def get_neighbours(self, nodes, k_neighbours, tree, heuristic):
        """Find k closest neighbours to self."""
        _, indices = tree.query([self.latlonrad], k=k_neighbours)
        indices = indices.tolist()[0]
        self.neighbours = []
        for i in indices:
            if self.id != i:
                if heuristic == "distance":
                    weight = self.get_distance_to(nodes[i]) + self.get_kinematics_to(nodes[i])
                else:
                    if self.dop <= 4.5:
                        weight = model.get_fuel_cost(self, nodes[i], "wind")
                        if np.arctan(self.latlon[2]/(np.sqrt(self.latlon[0]**2-self.latlon[1]**2))) < 1.117010721276371:
                            if np.arctan(self.latlon[1]/self.latlon[0]) < 1.138408533158592:
                                continue
                            else:
                                weight = model.get_optim_cost(self.latlon[3], nodes[i].latlon[3], self, nodes[i], "wind")
                        else:
                            weight = model.get_optim_cost(self.latlon[3], nodes[i].latlon[3], self, nodes[i], "wind")
                    else:
                        weight = model.get_optim_cost(self.latlon[3], nodes[i].latlon[3], self, nodes[i], "wind")
                self.neighbours.append(st.Neighbour(i, nodes[i], weight))


@dataclass
class Neighbour:
    id: int
    node: Node
    weight: int
    
    
    
    # def get_neighbours(self, nodes, k_neighbours, tree, heuristic):
    #     """Find k closest neighbours to self."""
    #     _, indices = tree.query([self.latlonrad], k=k_neighbours)
    #     indices = indices.tolist()[0]
    #     self.neighbours = []
    #     for i in indices:
    #         if self.id != i:
    #             if heuristic == "distance":
    #                 if self.get_dop(nodes[i]) <= 4.5:
    #                     weight = self.get_distance_to(nodes[i])
    #                 else:
    #                     lowest = self.get_dop(nodes[i]).sort()[0]
    #                     weight = lowest.get_distance(nodes[i])
    #             else:
    #                 weight = model.get_fuel_cost(self, nodes[i])
    #             self.neighbours.append(st.Neighbour(i, nodes[i], weight))
