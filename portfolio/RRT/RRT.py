# author: @yawen_x
# date: 12 nov. 23, updated 22 apr. 24 - 29 apr. 24
# purpose: rrt algorithm

from math import sqrt, atan2, cos, sin
from random import uniform
from collections import defaultdict, deque

from shapely import LineString, Polygon
import matplotlib.pyplot as plt


class RRT:
    def __init__(self, start, goal, env, step_size=5):
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

    def grow_tree(self, visualize=True, step_by_step=False):
        """
        grows tree for rrt! visualizes if asked to
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
                best_vertex = self.select_vertex()
                theta = uniform(0, 360)
                vertex_added = self.add_vertex(best_vertex, theta)

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

    def select_vertex(self):
        """
        returns vertex closest to our goal
        :return:
        """
        min_dist = float('inf')
        best_vertex = None

        # loop through vertices and return the one closest to goal
        for v in self.vertices:
            v_dist = sqrt((v[0] - self.goal[0])**2 + (v[1] - self.goal[1]) ** 2)
            if v_dist < min_dist:
                min_dist = v_dist
                best_vertex = v

        return best_vertex

    def add_vertex(self, vertex, theta):
        """
        adds new vertex a step_size in direction theta from given vertex;
        returns true if added successfully, false otherwise
        :param vertex:
        :param theta:
        :return:
        """
        # calculate new vertex
        new_x = vertex[0] + cos(theta) * self.step_size
        new_y = vertex[1] + sin(theta) * self.step_size
        new_vertex = tuple((new_x, new_y))

        # invalid vertex if there exists a collision in the path
        #   from given vertex to new vertex
        if self.is_collision(new_vertex, vertex):
            return False

        # invalid vertex if it grows out of bonds
        if new_vertex[0] < 0 or new_vertex[0] > self.env[0]:
            return False
        if new_vertex[1] < 0 or new_vertex[1] > self.env[1]:
            return False

        # otherwise add to graph
        new_edge = (vertex, new_vertex)
        self.vertices.append(new_vertex)
        self.edges.append(new_edge)
        return True

    def is_collision(self, v1, v2):
        """
        checks for collision going from one vertex to another
        :param v1:
        :param v2:
        :return:
        """
        path = LineString([v1, v2])

        # check for collision with each obstacle
        for obstacle in self.obstacle_polygons:
            if path.intersects(obstacle):
                return True

        return False

    def goal_reached(self, threshold=1):
        """
        checks if goal is within our tree
        :param threshold:
        :return:
        """
        temp = self.vertices.copy()

        # search for goal from end of current list of edges
        while len(temp) != 0:
            v = temp.pop()

            # if goal within threshold, we've reached it!
            if (self.goal[0] - self.step_size * threshold < v[0] < self.goal[0] + self.step_size * threshold
                    and self.goal[1] - self.step_size * threshold < v[1] < self.goal[1] + self.step_size * threshold):
                print()
                print("Tree grown!")
                print("---")
                print("VERTICES:\t", len(self.vertices))
                print("EDGES:\t\t", len(self.edges))
                return True

        return False

    def solve(self, visualize=True):
        self.grow_tree(visualize=False)
        self.bfs_on_edges(self.edges, self.start, self.vertices[-1])

        if visualize:

            # set up plot
            plt.figure(figsize=(6, 6))
            plt.plot(0, 0)
            plt.plot(self.env[0], self.env[1])

            # plot obstacles
            obstacles = self.env[2]
            for obstacle in obstacles:
                temp = obstacle.copy()
                temp.append(obstacle[0])
                x, y = zip(*temp)
                plt.plot(x, y, marker='o', linestyle='-', color='red', markersize=0)
                plt.fill(x, y, color="mistyrose")

            # plot start
            plt.plot(self.start[0], self.start[1], marker='o', linestyle='None', color='b', markersize=8)

            # plot goal
            plt.plot(self.goal[0], self.goal[1], marker='o', linestyle='None', color='gold', markersize=8)

            # plot graph
            for e in self.edges:
                x, y = zip(*e)
                plt.plot(x, y, marker='o', linestyle='-', color='b', markersize=4)

            # plot solution
            x, y = zip(*self.path)
            plt.plot(x, y, marker='o', linestyle='-', color='greenyellow', markersize=4)

            plt.show()

    def bfs_on_edges(self, edges, start, goal):
        """
        bfs on edges! finds path from start to goal
        :param edges:
        :param start:
        :param goal:
        :return:
        """
        # create dict from edges
        adj_list = defaultdict(list)
        for edge in edges:
            u, v = edge
            adj_list[u].append(v)
            adj_list[v].append(u)

        start, goal = tuple(start), tuple(goal)
        visited = set()
        queue = deque([(start, [start])])

        # while frontier not empty
        while queue:
            curr, path = queue.popleft()

            # base case: goal reached
            if curr == goal:
                self.path = path
                print()
                print("Path found!")
                print("---")
                print("PATH:", self.path)
                print("LENGTH:\t\t", len(self.path))
                print()
                return path

            # for each unvisited node
            if curr not in visited:
                visited.add(curr)
                neighbors = adj_list.get(curr, [])

                # loop through its neighbors
                for neighbor in neighbors:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))

        print("NO PATH FOUND.")
        return None
