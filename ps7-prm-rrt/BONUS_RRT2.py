# author: @yawen_xue
# date: 12 nov. 23
# purpose: rrt except i try to solve getting stuck somewhere

from math import cos, sin
from random import randint, uniform
from collections import Counter
from BONUS_RRT import RRT
import matplotlib.pyplot as plt


class RRT2(RRT):
    def __init__(self, start, goal, env, step_size=5):
        super().__init__(start, goal, env, step_size)

        # we're changing the goal randomly whenever we get stuck, for a new direction
        self.real_goal = goal
        self.fake_goal_moves = 0

    def stuck(self):
        """
        checks if we're stuck somewhere
        :return:
        """
        points = []
        threshold = 10

        # checks last 20 vertices for repeat points
        for u, v in self.edges[-20:]:
            points.append(u)
            points.append(v)

        # turn into dictionary to see if max exceeds threshold
        points_dict = Counter(points)

        # if the same point appears more times then the threshold permits, we're stuck
        for key in points_dict:
            if points_dict[key] >= threshold:
                return True

        return False

    def grow_tree(self):
        """
        grows rrt tree but we modify it
        :return:
        """
        # grow tree until we've reached the goal
        goal_reached = self.goal_reached()
        while not goal_reached:

            # keep attempting to add a vertex until we've done it
            vertex_added = False
            while not vertex_added:

                # sample direction for vertex
                point = self.sample()

                # check if stuck; handle by temporarily changing the goal for growth in a new direction
                if self.stuck() and self.goal == self.real_goal:
                    self.goal = (randint(0, self.env[0]), randint(0, self.env[1]))
                    # print("stuck!")
                    # print("new goal:", self.goal)

                # add new vertex
                vertex_added = self.add_vertex(point)

                # change back to real goal after 10 steps
                if self.goal != self.real_goal:
                    self.fake_goal_moves += 1

                if self.fake_goal_moves == 10:
                    # print("return to original goal")
                    self.goal = self.real_goal
                    self.fake_goal_moves = 0

            goal_reached = self.goal_reached()

    def grow_tree_vis(self, step_by_step=False):
        """
        same as grow_tree(), but now we visualize it
        :return:
        """
        # plot
        plt.figure(figsize=(6, 6))
        plt.plot(0, 0)
        plt.plot(100, 100)

        # plot obstacles
        obstacles = self.env[2]
        for obstacle in obstacles:
            temp = obstacle.copy()
            temp.append(obstacle[0])
            x, y = zip(*temp)
            plt.plot(x, y, marker='o', linestyle='-', color='red', markersize=0)
            plt.fill(x, y, color="mistyrose")

        # plot goal
        plt.plot(self.real_goal[0], self.real_goal[1], marker='o', color='gold', markersize=8)

        # grow tree until we've reached the goal
        goal_reached = self.goal_reached()
        while not goal_reached:

            # keep attempting to add a vertex until we've done it
            vertex_added = False
            while not vertex_added:

                # sample direction for vertex
                point = self.sample()

                # check if stuck; handle by temporarily changing the goal for growth in a new direction
                if self.stuck() and self.goal == self.real_goal:
                    self.goal = (randint(0, self.env[0]), randint(0, self.env[1]))
                    # print("stuck!")
                    # print("new goal:", self.goal)

                # add new vertex
                vertex_added = self.add_vertex(point)

                # change back to real goal after 10 steps
                if self.goal != self.real_goal:
                    self.fake_goal_moves += 1

                if self.fake_goal_moves == 10:
                    # print("return to original goal")
                    self.goal = self.real_goal
                    self.fake_goal_moves = 0

                # plot new vertex
                plt.plot(self.vertices[-1][0], self.vertices[-1][1], marker='o', color='b', markersize=4)

                # plot new edge
                if self.edges:
                    new_edge = self.edges[-1]
                    x, y = zip(*new_edge)
                    plt.plot(x, y, marker='o', linestyle='-', color='b', markersize=4)

                    if step_by_step:
                        plt.pause(0.01)
                        plt.show(block=False)

            goal_reached = self.goal_reached()

        plt.show(block=True)

    def add_vertex(self, point):
        """
        this time sampling gives us angles, and so we use angles instead of points
        :param point:
        :return:
        """
        # select best vertex (here, vertex closest to goal) to build an edge from
        best_vertex = self.select_best_vertex()

        # calculate direction from given point
        theta = point

        # find vertex
        new_x = best_vertex[0] + cos(theta) * self.step_size
        new_y = best_vertex[1] + sin(theta) * self.step_size
        new_vertex = tuple([new_x, new_y])

        # check for collision
        if self.is_collision(new_vertex, best_vertex):
            return False

        # return false if out of bounds
        if new_vertex[0] < 0 or new_vertex[0] > self.env[0]:
            return False
        if new_vertex[1] < 0 or new_vertex[1] > self.env[1]:
            return False

        # add to graph if no collision
        self.vertices.append(new_vertex)
        self.edges.append([best_vertex, new_vertex])
        return True

    def sample(self):
        """
        selects random direction for new vertex to be in
        :return:
        """
        theta = uniform(0, 360)

        return theta

    def goal_reached(self, threshold=0.5):
        """
        checks if we've reached the goal — that is, there is a point in vertices
        that is close enough to the goal
        :param threshold:
        :return:
        """
        temp = self.vertices.copy()

        # search for goal from end of current list of edges
        while len(temp) != 0:
            curr_v = temp.pop()

            # if goal within threshold, reached
            if (self.real_goal[0] - self.step_size * threshold < curr_v[0] < self.real_goal[0] + self.step_size * threshold
                    and self.real_goal[1] - self.step_size * threshold < curr_v[1] < self.real_goal[1] + self.step_size * threshold):
                print()
                print("tree grown!")
                print("vertices:\t", len(self.vertices))
                print("edges:\t\t", len(self.edges))
                print()
                return True

        return False
