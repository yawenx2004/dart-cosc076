# author: @yawen_xue
# date: 12 nov. 23
# purpose: control group to make sure rrt does better than chance

from random import choice
from BONUS_RRT import RRT


class RRTControl(RRT):
    def __init__(self, start, goal, env, step_size=5):
        super().__init__(start, goal, env, step_size)

    def select_best_vertex(self):
        return choice(self.vertices)