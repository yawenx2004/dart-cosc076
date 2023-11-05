# author: @yawen_xue
# date: 26 oct. 23
# purpose: hidden markov model to probabilistically solve robot location in maze

import sys
from PyQt6.QtWidgets import QApplication
from Maze import Maze
from RobotModel import RobotModel
from BONUS_RandomWalk import RandomWalk
from BONUS_VisualizePath import VisualizePath


class HMM:
    def __init__(self, robot_model, random_walk):
        # provided information
        self.maze = robot_model.maze
        self.sensor_readings = robot_model.sensor_readings
        self.start_state = self.get_start_state(robot_model.startloc)
        self.actual_path = robot_model.actual_path
        self.random_path = random_walk.path

        # what we're going to update throughout this algorithm
        self.state = self.start_state

        # for testing, to confirm sum of probabilities is 1
        self.sum_state = sum(self.state)

    def get_start_state(self, startloc):
        """
        helper function to get the start state based on the robot's starting location,
        which is known
        :param startloc:
        :return:
        """
        start_state = [0] * 16

        # convert starting location from coordinate pair to index
        index = startloc[1] * self.maze.width + startloc[0]

        # we're definitely on the starting location on time step 0
        start_state[index] = 1

        return start_state

    def predict(self):
        """
        updates probabilities of locations based on given knowledge about maze structure;
        probability changes in 5 different directions (n/s/e/w/staying put)
        :return:
        """
        new_state = [0] * 16

        # loop through current state and update probabilities
        for loc in range(1, len(self.state)):

            # if there is a non-zero probability of the robot being in this location,
            # then we can proceed from this location to adjacent ones
            if self.state[loc] != 0:
                # update probabilities for possible move directions n/s/e/w/staying put
                loc_probs = [0] * 5

                # if northward movement is valid:
                if loc + self.maze.width <= 15 and self.maze.is_floor_index(loc + self.maze.width):
                    loc_probs[1] = 0.25

                # if southward movement is valid
                if loc - self.maze.width >= 0 and self.maze.is_floor_index(loc - self.maze.width):
                    loc_probs[2] = 0.25

                # if eastward movement is valid
                if loc % self.maze.width < 3 and self.maze.is_floor_index(loc + 1):
                    loc_probs[3] = 0.25

                # if westward movement is valid
                if loc % self.maze.width > 0 and self.maze.is_floor_index(loc - 1):
                    loc_probs[4] = 0.25

                # probability of staying put equals sum of probabilities of not moving in any of these directions
                loc_probs[0] = 1 - sum(loc_probs)

                # update probabilities in all directions
                # we need to multiply everything by the probability of the current location
                new_state[loc] += self.state[loc]*loc_probs[0]
                if loc + self.maze.width <= 15:
                    new_state[loc + self.maze.width] += self.state[loc]*loc_probs[1]
                if loc - self.maze.width >= 0:
                    new_state[loc - self.maze.width] += self.state[loc]*loc_probs[2]
                if loc + 1 <= 15:
                    new_state[loc + 1] += self.state[loc]*loc_probs[3]
                if loc - 1 >= 0:
                    new_state[loc - 1] += self.state[loc]*loc_probs[4]

        # now we update state!!
        self.state = new_state

    def update(self, sensor_reading):
        """
        takes in information from sensor reading and updates state based upon that
        :param sensor_reading:
        :return:
        """
        # squares with the same color as the sensor reading are much more likely to be the current location
        for loc in range(0, len(self.state)):
            if self.maze.get_color_index(loc) == sensor_reading:
                self.state[loc] *= 0.88
            else:
                self.state[loc] *= 0.04

        self.normalize()

    def normalize(self):
        """
        helper function to make sure the sum of each probability vector is 1
        :return:
        """
        factor = 1/sum(self.state)
        for loc in range(0, len(self.state)):
            self.state[loc] *= factor

    def filter(self):
        """
        filtering algorithm; basically a wrapper function for
        :return:
        """
        states_history = []
        for i in range(0, len(self.sensor_readings)):
            self.predict()
            self.update(self.sensor_readings[i])
            states_history.append(self.state)
        return states_history

    def max_value(self, state):
        """
        returns most likely location
        :param state:
        :return:
        """
        max_value = 0
        indices = []
        for loc in range(0, len(state)):
            if state[loc] == max_value:
                indices.append(loc)
            elif state[loc] > max_value:
                max_value = state[loc]
                indices = [loc]

        # convert indices to coordinates
        coords = []
        for i in indices:
            x = i % self.maze.width
            y = i // self.maze.width
            c = [x, y]
            coords.append(c)

        return coords

    def solve(self):
        """
        runs algorithm and displays performance
        :return:
        """
        states_history = self.filter()
        mistakes = 0
        rand_mistakes = 0

        print("at each time step:")
        print("location\t\tprediction\t\trandom path")
        print("---\t\t\t\t---\t\t\t\t")

        # print each step
        for i in range(0, len(self.actual_path)):
            location = self.actual_path[i]
            prediction = self.max_value(states_history[i])
            rand = self.random_path[i]

            # mistake if incorrect prediction
            if location not in prediction:
                mistakes += 1

            if location != rand:
                rand_mistakes += 1

            print(str(self.actual_path[i]) + "\t\t\t" + str(prediction) + "\t\t\t" + str(rand))

        print()
        print(mistakes, "mistakes")
        print(rand_mistakes, "mistakes with random walk")

        # visualize
        app = QApplication(sys.argv)
        window = VisualizePath(self.maze, states_history, self.actual_path)
        sys.exit(app.exec())


# bit of test code
if __name__ == "__main__":
    maze1 = Maze("mazes/maze1.maz")
    test_robot = RobotModel(maze1)
    walk = RandomWalk(maze1)

    hmm = HMM(test_robot, walk)
    hmm.solve()
