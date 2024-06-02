# 3D-Route-Planning-in-Urban-Environments

# POSNAV 2022: Route Planning in Urban Environments Based on GNSS Performance

This repository contains the code and supplementary materials for the paper "Route Planning in Urban Environments Based on GNSS Performance," presented at the Positioning and Navigation for Intelligent Transport Systems (POSNAV) 2022 conference held on November 3-4, 2022, in Berlin.

## Overview

The research focuses on developing a route planning algorithm for Unmanned Aerial Vehicles (UAVs) operating in urban environments, where Global Navigation Satellite System (GNSS) performance is often degraded. The project implements an A* search algorithm to optimize UAV paths by considering various mission constraints, including GNSS performance metrics such as accuracy, integrity, availability, and continuity.

## Contents

- *Code: Implementation of the A* search algorithm in Python for UAV path planning.
- *Data*: Sample datasets provided by Spirent Communications, including GNSS performance metrics for urban environments.
- *Documentation*: Detailed documentation of the algorithm, methodology, and experimental results.

## Key Features

- *GNSS-aware Path Planning*: The algorithm incorporates GNSS performance metrics into the path planning process to enhance navigation accuracy and reliability in urban areas.
- *Multi-Constraint Optimization*: The route planning takes into account various constraints such as distance, no-fly zones, UAV kinematics, and GNSS quality.
- *Scenario-Based Analysis*: The algorithm is tested on different mission scenarios, including the shortest path and optimized GNSS performance paths.

## Authors

- Ibrahim Halil Turgut (Cranfield University)
- Ivan Petrunin (Cranfield University)
- Antonios Tsourdos (Cranfield University)
- Arjuna Flenner (GE Aviation Systems)
- Bo Peng (Spirent Communications PLC)
- Raphael Grech (Spirent Communications PLC)

## Acknowledgements

Special thanks to Spirent Communications PLC for providing the GNSS performance data and supporting this research.
