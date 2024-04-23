# author: @yawen_x
# date: 12 nov. 23, updated 22 apr. 24
# purpose: rrt algorithm but it tries to get unstuck

from math import sqrt, atan2, cos, sin
from random import uniform
from collections import defaultdict, deque

import matplotlib.pyplot as plt

from RRT import RRT

class RRT_unstuck(RRT):
    def __init__(self, start, goal, env, step_size=10):
        super().__init__(start, goal, env, step_size)

        # we want to change the goal randomly whenever we get stuck
        # so we could grow the tree toward elsewhere
        self.real_goal = goal       # keeps track of actual goal when we switch it up for unstuck purposes
        self.fake_goal_moves = 0    # keeps track of moves toward fake goal so you could switch back

    def grow_tree(self, visualize=False):
        pass

    def add_vertex(self):
        pass

    def select_vertex(self):
        pass

    def is_collision(self):
        pass
