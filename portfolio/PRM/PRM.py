# @author: yawen_x
# date: 11 nov. 23, updated 22 apr. 24
# purpose: prm algorithm

from random import uniform
from shapely import Polygon

from scipy.spatial import cKDTree
from scipy.interpolate import interp1d

import numpy as np
import matplotlib.pyplot as plt


class PRM:
    def __init__(self, robot, goal_config, obstacles, k=100, num_samples=200):
        self.robot = robot

        self.start_config = robot.start_config
        self.goal_config = goal_config
        self.obstacles = obstacles

        # turn obstacles into polygons for shapely collision checking
        self.obstacle_polygons = []
        for obstacle in obstacles:
            self.obstacle_polygons.append(Polygon(obstacle))

        # now onto the prm part
        self.k = k                          # connectivity: each vertex in the prm graph has at most k edges
        self.num_samples = num_samples      # density: we sample this many vertices

        # samples
        self.samples = [self.start_config, goal_config]
        self.kd_tree = None                 # speed: helps search nearby configurations

        # graph to search with PRMSolver
        self.edges = []
        self.start_config_reached = False   # keep building graph until exists edge that includes start_config...
        self.goal_config_reached = False    # and goal_config

    def get_roadmap(self, max_tries=10):
        """
        the meat: runs prm and returns the roadmap/graph to search
        :param max_tries:
        :return:
        """
        # keep generating graphs until we get one that contains start and end configs
        # (or if you exceed max_tries)
        counter = 0
        terminate = False

        while not terminate:
            # new graph, so let's wipe data from old tries
            self.samples = [self.start_config, self.goal_config]
            self.edges = []
            self.start_config_reached = False
            self.goal_config_reached = False

            # sample & add edges to create graph
            self.sample()
            self.add_edges()
            counter += 1
            print("TRYING GRAPH #" + str(counter))

            # good ending: you've found a graph that contains start and goal configs!
            if self.start_config_reached and self.goal_config_reached:
                terminate = True

            # bad ending: max tries exceeded
            if counter > max_tries:
                print("MAX TRIES EXCEEDED: No roadmap found after", counter, "tries")
                terminate = True
                return None, None, None

        # you've found a roadmap! return it for search
        print("Roadmap found after", counter, "tries")
        return self.start_config, self.goal_config, self.edges

    def sample(self):
        """
        samples discrete points within this continuous space; these will serve as the vertices
        :return:
        """
        # sample until we've reached number of samples specified
        while len(self.samples) < self.num_samples:
            print("Sampling vertices for PRM...")

            # generate random configuration
            rand_config = []

            # for an n-arm a config contains n angles
            for i in range(self.robot.num_joints):
                rand_config.append(uniform(0, 360))

            # check if random configuration collides with anything
            no_collisions = True
            if self.robot.collides_with(rand_config, self.obstacle_polygons):
                no_collisions = False

            # add random configuration to samples if no collisions
            if no_collisions:
                self.samples.append(rand_config)

        # update kd tree for neighbor-finding
        self.kd_tree = cKDTree(np.array(self.samples))

    def add_edges(self):
        """
        adds edges from each vertex to its nearest k neighbors,
        such that if two configs are connected by an edge
        then you can go from one to the other without collisions;
        now you've effectively built the roadmap
        :return:
        """
        # for each vertex, look at its k nearest neighbors
        for v in self.samples:
            neighbors = self.get_neighbors(v)
            print("Adding edges for PRM...")

            # for each neighbor u, check if valid edge exists between u and v
            # that is, if you can go from v to u without collision
            for u in neighbors:
                if u != v and not self.is_collision(v, u):
                    self.edges.append([v, u])

                # check if either u or v is the start or goal configuration
                # at which point you can stop building the graph
                if u == self.start_config or v == self.start_config:
                    self.start_config_reached = True
                if u == self.goal_config or v == self.goal_config:
                    self.goal_config_reached = True

    def get_neighbors(self, vertex):
        """
        gets nearest k neighbors using k-d tree
        :return:
        """
        neighbors = []
        distance, indices = self.kd_tree.query(vertex, self.k + 1)
        for i in indices:
            neighbors.append(self.samples[i])

        return neighbors

    def is_collision(self, config1, config2):
        """
        uses linear interpolation to check for collision between 2 configs
        :param config1:
        :param config2:
        :return:
        """
        # interpolate!
        t_values = np.linspace(0, 1, 10)
        interpolator = interp1d([0, 1], np.vstack([config1, config2]), axis=0, kind='linear', fill_value='extrapolate')
        interpolated_configs = interpolator(t_values)

        # for each interpolated configuration, check for collisions with obstacles
        for c in interpolated_configs:
            if self.robot.collides_with(c, self.obstacle_polygons):
                return True

        return False

    ''' all code below is for visualization at matplotlib '''
    def visualize_config(self, config, marker='o', linestyle='-', color='b', markersize=2):
        """
        helper function to visualize specified configuration
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
        helper function to visualizes environment (start & goal, obstacles, current config of arm)
        :return:
        """
        plt.figure(figsize=(6, 6))

        # start & goal
        self.visualize_config(self.robot.start_config, color="r")
        self.visualize_config(self.goal_config, color='gold')

        # obstacles
        self.visualize_obstacles()

        # current config of arm
        self.visualize_config(self.robot.config)

        # plt
        plt.title('environment')
        plt.gca().set_aspect('equal')
        plt.show()

    def visualize_samples(self):
        """
        helper function to visualize all samples; only works for 2r robots since this is in 2d space
        :return:
        """
        if len(self.samples[0]) == 2:
            plt.figure(figsize=(6, 6))

            # plot sample configs
            x, y = zip(*self.samples)
            plt.plot(x, y, marker='o', linestyle='None', color='b', markersize=4)

            # plot edges
            for e in self.edges:
                x, y = zip(*e)
                plt.plot(x, y, marker='o', linestyle='-', color='b', markersize=4)

            # plot start & goal
            plt.plot(self.robot.config[0], self.robot.config[1], marker='o', linestyle='-', color='r', markersize=6)
            plt.plot(self.goal_config[0], self.goal_config[1], marker='o', linestyle='-', color='gold', markersize=6)

            # labels
            plt.title('samples')
            plt.gca().set_aspect('equal')
            plt.show()

        else:
            print("PASS. Cannot display 3D points on 2D plane.")

    def visualize_configs(self):
        """
        helper function to visualize all configs in roadmap
        :return:
        """
        plt.figure(figsize=(6, 6))

        for e in self.edges:

            # start & end configs
            u = e[0]
            v = e[1]

            self.visualize_obstacles()
            self.visualize_config(v)
            self.visualize_config(u)
            self.visualize_config(self.robot.start_config, color="r")
            self.visualize_config(self.goal_config, color="gold")

            plt.title('edges')
            plt.gca().set_aspect('equal')

        plt.show()
