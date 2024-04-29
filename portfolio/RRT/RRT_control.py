# author: @yawen_x
# date: 12 nov. 23, updated 22 apr. 24
# purpose: test rrt!

from random import choice
from RRT import RRT


class RRT_control(RRT):
    def __init__(self, start, goal, env, step_size=5):
        super().__init__(start, goal, env, step_size)

    def select_vertex(self):
        """
        instead of selecting the best vertex you just select a random one
        :return:
        """
        return choice(self.vertices)
