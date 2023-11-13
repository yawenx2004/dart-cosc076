# author: @yawen_xue
# date: 12 nov. 23
# purpose: rrt except i don't use physics

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

        # obstacle polygons for collision check
        self.obstacle_polygons = []
        for obstacle in env[2]:
            self.obstacle_polygons.append(Polygon(obstacle))

        # for growing tree
        self.step_size = step_size
        self.vertices = [start]
        self.edges = []
        self.path = []

    def grow_tree(self):
        """
        grows rrt tree!
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
                vertex_added = self.add_vertex(point)

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

        # grow tree until we've reached the goal
        goal_reached = self.goal_reached()
        while not goal_reached:

            # keep attempting to add a vertex until we've done it
            vertex_added = False
            while not vertex_added:

                # sample direction for vertex
                point = self.sample()
                vertex_added = self.add_vertex(point)

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
        adds vertex step_size away from a selected best vertex in a given direction
        :param point:
        :return:
        """
        # select best vertex (here, vertex closest to goal) to build an edge from
        best_vertex = self.select_best_vertex()

        # calculate direction from given point
        theta = atan2(point[1] - best_vertex[1], point[0] - best_vertex[0])

        # find vertex
        new_x = best_vertex[0] + cos(theta) * self.step_size
        new_y = best_vertex[1] + sin(theta) * self.step_size
        new_vertex = tuple([new_x, new_y])

        # check for collision
        if self.is_collision(new_vertex, best_vertex):
            return False

        # add to graph if no collision
        new_edge = (best_vertex, new_vertex)
        self.vertices.append(new_vertex)
        self.edges.append(new_edge)
        return True

    def select_best_vertex(self):
        """
        finds best vertex — here, vertex closest to goal
        :return:
        """
        min_dist = float('inf')
        best_vertex = None

        # loop through vertices and find one closest to goal
        for v in self.vertices:
            v_dist = self.dist_from_goal(v)
            if v_dist < min_dist:
                min_dist = v_dist
                best_vertex = v

        return best_vertex

    def is_collision(self, vertex, prev):
        """
        checks for collision between each pair of vertices and all obstacles
        :param vertex:
        :param prev:
        :return:
        """
        l = LineString([vertex, prev])

        # for each obstacle
        for obstacle in self.obstacle_polygons:
            if l.intersects(obstacle):
                return True

        return False

    def dist_from_goal(self, vertex):
        """
        uses pythagorean theorem to calculate distance between given vertex and goal
        :param vertex:
        :return:
        """
        dist = sqrt((vertex[0] - self.goal[0]) ** 2 + (vertex[1] - self.goal[1]) ** 2)
        return dist

    def sample(self):
        """
        selects random point; new vertex will be a step in that direction
        :return:
        """
        x = uniform(0, self.env[0])
        y = uniform(0, self.env[1])
        point = (x, y)

        return point

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
            if (self.goal[0] - self.step_size * threshold < curr_v[0] < self.goal[0] + self.step_size * threshold
                    and self.goal[1] - self.step_size * threshold < curr_v[1] < self.goal[1] + self.step_size * threshold):
                print()
                print("tree grown!")
                print("vertices:\t", len(self.vertices))
                print("edges:\t\t", len(self.edges))
                print()
                return True

        return False

    def solve(self, visualize=True):
        """
        runs rrt to grow tree, then runs bfs to search path through tree
        :param visualize:
        :return:
        """
        self.grow_tree()
        self.bfs_on_edges(self.edges, self.start, self.vertices[-1])

        if visualize:
            self.visualize_solution()

    def bfs_on_edges(self, edges, start, goal):
        """
        bfs! finds path from edges
        :param edges:
        :param start:
        :param goal:
        :return:
        """
        # create dict from edges
        adjacency_list = defaultdict(list)
        for edge in edges:
            u, v = edge
            adjacency_list[u].append(v)
            adjacency_list[v].append(u)

        start, goal = tuple(start), tuple(goal)
        visited = set()
        queue = deque([(start, [start])])

        # while frontier not empty
        while queue:
            current, path = queue.popleft()

            # base case: goal reached
            if current == goal:
                self.path = path
                print()
                print("path:", self.path)
                print("length:\t\t", len(self.path))
                print()
                return path

            # for each unvisited node
            if current not in visited:
                visited.add(current)
                neighbors = adjacency_list.get(current, [])

                # loop through its neighbors
                for neighbor in neighbors:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))

        print("no path found")
        return None

    def visualize_solution(self):
        """
        visualizes environment
        :return:
        """
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

    def visualize_env(self):
        """
        visualizes environment
        :return:
        """
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

        plt.show()
