# @author: yawen_x
# date: 11 nov. 23, updated 22 apr. 24
# purpose: robot arm model for prm

from math import pi, sin, cos
from shapely import LineString
import matplotlib.pyplot as plt


class ArmRobot:
    def __init__(self, num_joints, start_config):
        self.num_joints = num_joints
        self.start_config = start_config

        # we begin at starting configuration
        self.config = start_config

    def set_config(self, config):
        """
        helper function to set joint angles
        :param config:
        :return:
        """
        if len(config) != self.num_joints:
            print("ERROR. Mismatch between configuration size and number of angles.")
        else:
            self.config = config

    def forward_kinematics(self, config):
        """
        calculates location of joints based on angles in given configuratino
        :param config:
        :return:
        """
        # first anchor at origin
        joint_loc = [[0, 0]]

        # for each angle in configuration, calculate endpoint of corresponding joint
        theta = 0
        for i in range(len(config)):
            theta += config[i] * pi / 180

            # each point builds upon previous point
            x = joint_loc[i][0] + cos(theta)
            y = joint_loc[i][1] + sin(theta)
            joint_loc.append([x, y])

        return joint_loc

    def collides_with(self, config, obstacles):
        """
        checks if arm in given configuration collides with obstacles in given array
        :param config:
        :param obstacles:
        :return:
        """
        joint_loc = self.forward_kinematics(config)

        # for each link of joint
        for i in range(1, len(joint_loc)):

            # use shapely library to check interaction...
            start = joint_loc[i - 1]
            end = joint_loc[i]
            link = LineString([start, end])

            # ... with each obstacle in obstacle list
            for obstacle in obstacles:
                if link.intersects(obstacle):
                    return True

        return False

    def visualize(self):
        joint_loc = self.forward_kinematics(self.config)
        x, y = zip(*joint_loc)

        # matplotlib!
        plt.figure(figsize=(6, 6))
        plt.plot(x, y, marker='o', linestyle='-', color='b', linewidth=2)
        plt.title('robot arm')
        plt.gca().set_aspect('equal')
        plt.show()


# bit of test code
if __name__ == "__main__":
    # create arm; see it
    r = ArmRobot(3, [30, -30, 0])
    r.visualize()
