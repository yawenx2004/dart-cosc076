# author: @yawen_x
# date: 12 nov. 23, updated 22 apr. 24
# purpose: rrt algorithm but it tries to get unstuck

from math import sqrt, atan2, cos, sin
from random import uniform, randint
from collections import Counter

import matplotlib.pyplot as plt

from RRT import RRT

class RRT_unstuck(RRT):
    def __init__(self, start, goal, env, step_size=5):
        super().__init__(start, goal, env, step_size)

        # we want to change the goal randomly whenever we get stuck
        # so we could grow the tree toward elsewhere
        self.real_goal = goal       # keeps track of actual goal when we switch it up for unstuck purposes
        self.real_goal_moves = 0
        self.fake_goal_moves = 0    # keeps track of moves toward fake goal so you could switch back

    def stuck(self, threshold=10, sample_size=20):
        points = []

        # checks last sample_size vertices for repeat points
        for u, v, in self.edges[-sample_size:]:
            points.append(u)
            points.append(v)

        # check if any point repeats more times than threshold permits
        #   if so we are STUCK
        points_dict = Counter(points)
        for key in points_dict:
            if points_dict[key] >= threshold:
                return True

        return False

    def grow_tree(self, visualize=True, step_by_step=False):
        """
        modified to change goal temporarily if we get stuck
        :param visualize:
        :param step_by_step:
        :return:
        """
        if visualize:
            plt.figure(figsize=(6, 6))
            plt.plot(0, 0)
            plt.plot(100, 100)

            # plot start
            plt.plot(self.start[0], self.start[1], marker='o', linestyle='None', color='b', markersize=8)

            # plot goal
            plt.plot(self.goal[0], self.goal[1], marker='o', linestyle='None', color='gold', markersize=8)

            # plot obstacles
            obstacles = self.env[2]
            for obstacle in obstacles:

                # seal shape
                temp = obstacle.copy()
                temp.append(obstacle[0])

                x, y = zip(*temp)
                plt.plot(x, y, marker='o', linestyle='-', color='red', markersize=0)
                plt.fill(x, y, color="mistyrose")

        # keep growing tree until we reach goal
        while not self.goal_reached():

            # keep attempting to add vertex until we've succeeded
            vertex_added = False
            while not vertex_added:

                # try to add new point branching from best vertex in random direction
                theta = uniform(0, 360)

                # check if stuck
                #   handle stuck by temporarily changing goal to increase exploration
                if self.stuck and self.goal == self.real_goal:
                    if self.real_goal_moves >= 20:
                        self.goal = (randint(0, self.env[0]), randint(0, self.env[1]))
                        self.real_goal_moves = 0
                        print("STUCK! Goal changed temporarily.")
                    else:
                        self.goal = self.real_goal

                # plot goal
                plt.plot(self.goal[0], self.goal[1], marker='o', linestyle='None', color='gold', markersize=8)

                best_vertex = self.select_vertex()
                vertex_added = self.add_vertex(best_vertex, theta)

                # change back to real goal after 10 steps
                if self.goal != self.real_goal:
                    self.fake_goal_moves += 1
                else:
                    self.real_goal_moves += 1

                if self.fake_goal_moves == 10:
                    print("MAX FAKE GOAL STEPS. Revert to real goal.")
                    self.goal = self.real_goal
                    self.fake_goal_moves = 0

                # plot tree growing
                if visualize:
                    plt.plot(self.vertices[-1][0], self.vertices[-1][1], marker='o', color='b', markersize=4)

                    if self.edges:
                        new_edge = self.edges[-1]
                        x, y = zip(*new_edge)
                        plt.plot(x, y, marker='o', linestyle='-', color='b', markersize=4)

                        if step_by_step:
                            plt.pause(0.01)
                            plt.show(block=False)

        if visualize:
            plt.show(block=True)

    def goal_reached(self, threshold=1):
        """
        modified to check for REAL goal
        :param threshold:
        :return:
        """
        temp = self.vertices.copy()

        # search for goal from end of current list of edges
        while len(temp) != 0:
            v = temp.pop()

            # if goal within threshold, we've reached it!
            if (self.real_goal[0] - self.step_size * threshold < v[0] < self.real_goal[0] + self.step_size * threshold
                    and self.real_goal[1] - self.step_size * threshold < v[1] < self.real_goal[1] + self.step_size * threshold):
                print()
                print("Tree grown!")
                print("---")
                print("VERTICES:\t", len(self.vertices))
                print("EDGES:\t\t", len(self.edges))
                return True

        return False