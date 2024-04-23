# author: @yawen_x
# date: 12 nov. 23, updated 22 apr. 24
# purpose: rrt algorithm

from math import sqrt, atan2, cos, sin
from random import uniform
from collections import defaultdict, deque

from shapely import LineString, Polygon
import matplotlib.pyplot as plt


class RRT:
    def __init__(self, start, goal, env, step_size=10):
        self.start = start
        self.goal = goal
        self.env = env

        # extract obstacle polygons from environment for collision checks
        self.obstacle_polygons = []
        for obstacle in env[2]:
            self.obstacle_polygons.append(Polygon(obstacle))

        # this is where your tree will grow
        self.step_size = step_size
        self.vertices = [start]
        self.edges = []
        self.path = []
