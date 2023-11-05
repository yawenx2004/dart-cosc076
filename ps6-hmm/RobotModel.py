# author: @yawen_xue
# date: 28 oct. 23
# purpose: to model robot

from random import choice, uniform
from Maze import Maze


class RobotModel:
    def __init__(self, maze, num_observations=16):
        self.maze = maze
        self.startloc = maze.robotloc.copy()
        self.sensor_readings = []   # what the robot believes -- just a sequence of sensor readings
        self.actual_path = []       # what the robot actually does

        # get data, for hmm solver
        self.get_data(num_observations)

    def get_data(self, num_observations):
        """
        obtain data for model
        :param num_observations:
        :return:
        """
        for i in range(0, num_observations):
            self.observe()

    def observe(self):
        """
        models robot moving through maze and returning movement (attempt) + color observation;
        generates a random move (n/s/e/w), and gets color
        :return:
        """
        # choose random move
        moves = [[0, 1], [0, -1], [1, 0], [-1, 0]]  # n, s, e, w
        move = choice(moves)

        # move robot if legal
        newloc = [self.maze.robotloc[0] + move[0], self.maze.robotloc[1] + move[1]]
        if self.maze.is_floor(newloc[0], newloc[1]):
            self.maze.robotloc = newloc

        # get new sensor input
        color = self.maze.get_color(self.maze.robotloc[0], self.maze.robotloc[1])
        sensor_reading = self.color_sensor(color)
        self.sensor_readings.append(sensor_reading)
        self.actual_path.append(self.maze.robotloc)

    def color_sensor(self, actual_color):
        """
        helper function to represent our imperfect sensor;
        generates random probability to determine if returned color is same as actual color
        :param actual_color:
        :return:
        """
        colors = ["R", "G", "B", "Y"]
        colors.remove(actual_color)
        rand_prob = uniform(0, 1)

        # 0.88 probability of accuracy
        if rand_prob <= 0.88:
            return actual_color

        # else return any of the other colors, at random
        else:
            return choice(colors)


# bit of test code
if __name__ == "__main__":
    maze1 = Maze("mazes/maze1.maz")
    test_robot = RobotModel(maze1)
    print(test_robot.sensor_readings)
    print(test_robot.actual_path)
