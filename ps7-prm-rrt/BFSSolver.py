# author: @yawen_xue
# date: 11 nov. 23
# purpose: runs bfs on prm roadmap; solves

from collections import defaultdict, deque
import matplotlib.pyplot as plt

from ArmRobot import ArmRobot
from PRM import PRM


class BFSSolver:
    def __init__(self, robot, prm):
        self.robot = robot
        self.prm = prm
        self.goal = prm.goal
        self.path = []
        self.nodes_searched = 0

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
            u, v = tuple(map(tuple, edge))
            adjacency_list[u].append(v)
            adjacency_list[v].append(u)

        start, goal = tuple(start), tuple(goal)
        visited = set()
        queue = deque([(start, [start])])

        # while frontier not empty
        while queue:
            current, path = queue.popleft()
            self.nodes_searched += 1

            # base case: goal reached
            if current == goal:
                return path

            # for each unvisited node
            if current not in visited:
                visited.add(current)
                neighbors = adjacency_list.get(current, [])

                # loop through its neighbors
                for neighbor in neighbors:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))

        print("No path found in roadmap")
        self.prm.visualize_samples()
        self.prm.visualize_configs()
        return None

    def solve(self, visualize=True):
        """
        solves problem by running bfs on prm-generated edges
        :param visualize:
        :return:
        """
        # environment
        self.prm.visualize_env()

        # run prm and get roadmap
        start, goal, edges = self.prm.get_roadmap()
        if edges is None:
            return

        # run bfs
        self.path = self.bfs_on_edges(edges, start, goal)

        # report
        print()
        if self.path:
            print("Solution found after searching", self.nodes_searched, "nodes!")
            print("---")
            print("path:", self.path)
            print("length:", len(self.path))
            print()
        else:
            print("No solution found")

        # display pt. 2 (optional)
        if visualize:
            self.visualize()

    def visualize(self):
        """
        displays plot for each configuration
        :return:
        """
        if self.path:
            plt.figure(figsize=(6, 6))

            # visualize for each configuration
            for config in self.path:
                plt.clf()

                # display parts
                self.prm.visualize_obstacles()
                self.prm.visualize_config(self.goal, color='gold')
                self.prm.visualize_config(config)

                # labels; square aspect ratio
                plt.title('robot arm')
                plt.gca().set_aspect('equal')

                # to show movement
                plt.show(block=False)
                plt.pause(0.1)

        plt.show(block=True)


# bit of test code
if __name__ == "__main__":
    r = ArmRobot(4, [0, 0, 0, 300])
    obstacles = [[(-1, -0.25), (-1, 1.5), (-1.5, 1.5)], [(2.5, 1.75), (2.5, 2.25), (2, 2.25), (2, 1.75)], [(-0.5, -0.5), (-0.5, -1), (-1, -1)]]
    prm = PRM(r, [120, 330, 0, 0], obstacles, k=5, num_samples=10000)
    bs = BFSSolver(r, prm)

    bs.solve()
