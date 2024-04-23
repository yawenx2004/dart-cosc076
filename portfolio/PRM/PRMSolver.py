# @author: yawen_x
# date: 11 nov. 23, updated 22 apr. 24
# purpose: get map using prm; use bfs to search map & solve

from collections import deque, defaultdict
import matplotlib.pyplot as plt

from ArmRobot import ArmRobot
from PRM import PRM


class PRMSolver:
    def __init__(self, robot, prm):
        self.robot = robot
        self.prm = prm
        self.goal_config = prm.goal_config

        self.path = []
        self.nodes_searched = 0

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
            u, v = tuple(map(tuple, edge))
            adj_list[u].append(v)
            adj_list[v].append(u)

        start, goal = tuple(start), tuple(goal)

        # bfs things
        visited = set()
        queue = deque([(start, [start])])   # node + path

        # while frontier not empty
        while queue:
            curr, path = queue.popleft()
            self.nodes_searched += 1
            print("Searching with BFS...")

            # base case: goal reached
            if curr == goal:
                return path

            # for each unvisited node... visit it
            if curr not in visited:
                visited.add(curr)
                neighbors = adj_list.get(curr, [])

                # loop through its neighbors, and add unvisited ones to queue
                for neighbor in neighbors:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))

        # we've run bfs! now report
        print("ERROR. No path found in roadmap.")
        self.prm.visualize_samples()
        self.prm.visualize_configs()
        return None

    def solve(self, visualize=True):
        """
        runs bfs on prm-generated edges
        :param visualize:
        :return:
        """
        # first let's display the environment
        # self.prm.visualize_env()

        # run prm to get roadmap
        start, goal, edges = self.prm.get_roadmap()
        if edges is None:
            return

        # now run bfs on roadmap
        self.path = self.bfs_on_edges(edges, start, goal)

        # report!
        print()
        if self.path:
            print("Solution found after searching", self.nodes_searched, "nodes!")
            print("---")
            print("PATH:", self.path)
            print("LENGTH:", len(self.path))
            print()
        else:
            print("No solution found :(")

        # display solution if asked to
        if visualize:
            self.visualize()

    def visualize(self):
        """
        helper function to visualize solution
        :return:
        """
        if self.path:
            plt.figure(figsize=(6, 6))

            # visualize for each configuration
            for config in self.path:
                plt.clf()

                # display parts
                self.prm.visualize_obstacles()
                self.prm.visualize_config(self.goal_config, color='gold')
                self.prm.visualize_config(config)

                # labels; square aspect ratio
                plt.title('robot arm')
                plt.gca().set_aspect('equal')

                # to show movement
                plt.show(block=False)
                plt.pause(1)

        plt.show(block=True)


# bit of test code
if __name__ == "__main__":
    r = ArmRobot(4, [0, 0, 0, 300])
    obstacles = [[(-1, -0.25), (-1, 1.5), (-1.5, 1.5)],
                 [(2.5, 1.75), (2.5, 2.25), (2, 2.25), (2, 1.75)],
                 [(-0.5, -0.5), (-0.5, -1), (-1, -1)]]
    prm = PRM(r, [120, 330, 0, 0], obstacles, k=5, num_samples=10000)
    solver = PRMSolver(r, prm)

    solver.solve()
