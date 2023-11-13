# author: @yawen_xue
# date: 11 nov. 23
# purpose: robot model for prm

from math import pi, sin, cos
from shapely import LineString
import matplotlib.pyplot as plt


class ArmRobot:
    def __init__(self, num_joints, starting_config):
        self.num_joints = num_joints
        self.starting_config = starting_config
        self.config = starting_config

    def set_config(self, config):
        """
        helper function to set joint angles
        :param config:
        :return:
        """
        if len(config) != self.num_joints:
            print("Pass. Incorrect number of angles.")
        else:
            self.config = config

    def forward_kinematics(self, config):
        """
        calculates location of joints based on angles
        :param config:
        :return:
        """
        loc = [[0, 0]]

        # loop through configuration
        theta = 0
        for i in range(len(config)):
            theta += config[i] * pi / 180
            x = loc[i][0] + cos(theta)
            y = loc[i][1] + sin(theta)
            loc.append([x, y])

        return loc

    def collides_with(self, config, obstacles):
        """
        checks if arm collides with given obstacle
        :param config:
        :param obstacles:
        :return:
        """
        loc = self.forward_kinematics(config)

        # for each link
        for i in range(1, len(loc)):
            start = loc[i - 1]
            end = loc[i]
            link = LineString([start, end])

            # for each obstacle
            for obstacle in obstacles:
                if link.intersects(obstacle):
                    return True

        return False

    def visualize(self):
        """
        displays using matplotlib
        :return:
        """
        loc = self.forward_kinematics(self.config)
        x, y = zip(*loc)

        # labels; square aspect ratio
        plt.figure(figsize=(6, 6))
        plt.plot(x, y, marker='o', linestyle='-', color='b', linewidth=2)
        plt.title('robot arm')
        plt.gca().set_aspect('equal')
        plt.show()


# bit of test code
if __name__ == "__main__":
    r = ArmRobot(3, [30, -30, 0])
    r.visualize()
