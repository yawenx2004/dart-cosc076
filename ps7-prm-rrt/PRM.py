# author: @yawen_xue
# date: 11 nov. 23
# purpose: prm algorithm

from random import uniform
from shapely import Polygon
from scipy.spatial import cKDTree
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt


class PRM:
    def __init__(self, robot, goal, obstacles, k=100, num_samples=200):
        self.robot = robot
        self.start = robot.starting_config
        self.goal = goal
        self.obstacles = obstacles

        # turn obstacles into polygons for collision checking
        self.obstacle_polygons = []
        for obstacle in obstacles:
            self.obstacle_polygons.append(Polygon(obstacle))

        # prm
        self.k = k
        self.num_samples = num_samples
        self.samples = [self.start, goal]
        self.kd_tree = None

        # graph to search
        self.edges = []
        self.start_in_edges = False
        self.goal_in_edges = False

    def get_roadmap(self, max_tries=10):
        """
        runs prm and returns a graph to search
        :return:
        """
        # keep generating graphs until they contain start and end
        counter = 0
        terminate = False

        while not terminate:
            # blank slate
            self.samples = [self.start, self.goal]
            self.edges = []
            self.start_in_edges = False
            self.goal_in_edges = False

            # sample again
            self.sample()
            self.add_edges()
            counter += 1
            print("Trying graph #" + str(counter))

            # terminate if semi-valid graph found
            if self.start_in_edges and self.goal_in_edges:
                terminate = True

            # terminate if tries exceeds max tries
            if counter > max_tries:
                print("No roadmap found after", counter, "tries")
                terminate = True
                return None, None, None

        print("Roadmap found after", counter, "tries")
        return self.start, self.goal, self.edges

    def collision_checker(self, config1, config2):
        """
        checks collision between two configurations using linear interpolation
        :return:
        """
        # interpolate!
        t_values = np.linspace(0, 1, 10)
        interpolator = interp1d([0, 1], np.vstack([config1, config2]), axis=0, kind='linear', fill_value='extrapolate')
        interpolated_configs = interpolator(t_values)

        # for each interpolated configuration, check for collisions
        for c in interpolated_configs:
            if self.robot.collides_with(c, self.obstacle_polygons):
                return True

        return False

    def sample(self):
        """
        generates random configurations
        :return:
        """
        while len(self.samples) < self.num_samples:
            rand_config = []
            for i in range(self.robot.num_joints):
                rand_config.append(uniform(0, 360))

            # add configurations to samples if fits criteria
            free_space = True
            if self.robot.collides_with(rand_config, self.obstacle_polygons):
                free_space = False

            if free_space:
                self.samples.append(rand_config)

        # update kd tree for neighbor-finding
        self.kd_tree = cKDTree(np.array(self.samples))

    def add_edges(self):
        """
        adds edges from each valid vertex to its nearest k neighbors
        :return:
        """
        # for each vertex get k nearest neighbors
        for v in self.samples:
            neighbors = self.nearest_k_neighbors(v)

            # for each neighbor
            for u in neighbors:
                if u != v and not self.collision_checker(v, u):
                    self.edges.append([v, u])

                    # check for start
                    if u == self.start or v == self.start:
                        self.start_in_edges = True

                    # check for goal
                    if u == self.goal or v == self.goal:
                        self.goal_in_edges = True

    def nearest_k_neighbors(self, vertex):
        """
        finds k nearest neighbors using k-d tree
        :return:
        """
        neighbors = []
        distance, indices = self.kd_tree.query(vertex, self.k + 1)
        for i in indices:
            neighbors.append(self.samples[i])

        return neighbors

    def visualize_config(self, config, marker='o', linestyle='-', color='b', markersize=2):
        """
        helper function to visualize each configuration
        :param config:
        :param marker:
        :param linestyle:
        :param color:
        :param markersize:
        :return:
        """
        loc = self.robot.forward_kinematics(config)
        x, y = zip(*loc)
        plt.plot(x, y, marker=marker, linestyle=linestyle, color=color, markersize=markersize, linewidth=1)

    def visualize_obstacles(self):
        """
        helper function to visualize all obstacles
        :return:
        """
        for obstacle in self.obstacles:
            temp = obstacle.copy()
            temp.append(obstacle[0])
            x, y = zip(*temp)
            plt.plot(x, y, marker='o', linestyle='-', color='red', markersize=0)
            plt.fill(x, y, color="mistyrose")

    def visualize_env(self):
        """
        visualizes environment (i.e. goal, obstacles, robot arm)
        :return:
        """
        plt.figure(figsize=(6, 6))

        self.visualize_config(self.goal, color='gold')
        self.visualize_config(self.robot.starting_config, color="r")
        self.visualize_obstacles()
        self.visualize_config(self.robot.config)

        # labels; square aspect ratio
        plt.title('environment')
        plt.gca().set_aspect('equal')
        plt.show()

    def visualize_samples(self):
        """
        only works for 2r robots; for testing
        :return:
        """
        if len(self.samples[0]) == 2:
            plt.figure(figsize=(6, 6))

            # samples
            x, y = zip(*self.samples)
            plt.plot(x, y, marker='o', linestyle='None', color='b', markersize=4)

            # edges
            for e in self.edges:
                x, y = zip(*e)
                plt.plot(x, y, marker='o', linestyle='-', color='b', markersize=4)

            # start and goal
            plt.plot(self.robot.config[0], self.robot.config[1], marker='o', linestyle='-', color='r', markersize=6)
            plt.plot(self.goal[0], self.goal[1], marker='o', linestyle='-', color='gold', markersize=6)

            # labels
            plt.title('samples')
            plt.gca().set_aspect('equal')
            plt.show()

        else:
            print("Pass.")

    def visualize_configs(self):
        """
        visualizes all possible configurations found in roadmap
        :return:
        """
        plt.figure(figsize=(6, 6))

        for e in self.edges:

            # starting and ending configurations
            u = e[0]
            v = e[1]

            self.visualize_obstacles()
            self.visualize_config(v)
            self.visualize_config(u)
            self.visualize_config(self.robot.starting_config, color="r")
            self.visualize_config(self.goal, color="gold")

            # labels; square aspect ratio
            plt.title('edges')
            plt.gca().set_aspect('equal')

        plt.show()
