# author: @yawen_xue
# date: 3 nov. 23
# purpose: generalized viterbi algorithm

from Maze import Maze
from RobotModel import RobotModel
from BONUS_RandomWalk import RandomWalk


class Viterbi:
    def __init__(self, observations, states, i_prob, t_prob, e_prob):
        self.observations = observations
        self.states = states
        self.i_prob = i_prob    # initial probabilities
        self.t_prob = t_prob    # transition probabilities
        self.e_prob = e_prob    # emission probabilities

    def viterbi(self):
        """
        viterbi algorithm; uses transmission probabilities and emission probabilities
        to calculate most likely path in conjunction with observations
        :return:
        """
        # 2d array of timestep to state
        viterbi_table = [[0] * len(self.states) for _ in range(len(self.observations))]

        # 2d array of backpointers
        backpointers = [[0] * len(self.states) for _ in range(len(self.observations))]

        # for conversion
        color_to_index = {"R": 0, "G": 1, "B": 2, "Y": 3}

        # initialize for first observation
        for i in range(0, len(self.states)):
            viterbi_table[0][i] = self.i_prob[i] * self.e_prob[i][color_to_index[self.observations[0]]]
            backpointers[0][i] = 0

        # for each subsequent observation-state pair
        for o in range(1, len(self.observations)):
            for s1 in range(0, len(self.states)):
                max_prob = 0
                best_state = 0

                # check next state
                for s2 in range(0, len(self.states)):

                    # probability of meeting specified conditions which is the product of
                    #  prob(most likely path leading to s2 at timestep o - 1)
                    #  prob(going from s2 to s1)
                    #  prob(observing specified color in s2)
                    prob = (viterbi_table[o - 1][s2] * self.t_prob[s2][s1] *
                            self.e_prob[s2][color_to_index[self.observations[o]]])

                    if prob > max_prob:
                        max_prob = prob
                        best_state = s2

                viterbi_table[o][s1] = max_prob
                backpointers[o][s1] = best_state

        # last time step, most likely state
        final_state = viterbi_table[len(self.observations) - 1].index(max(viterbi_table[len(self.observations) - 1]))

        # build path from backpointers
        path = [final_state]
        for i in range(len(self.observations) - 1, 0, -1):
            prev = backpointers[i][final_state]
            path.insert(0, prev)

        return path


class ViterbiSolver:
    def __init__(self, robot_model, random_walk):
        self.maze = robot_model.maze
        self.actual_path = robot_model.actual_path
        self.random_path = random_walk.path

        # observations = sensor readings
        self.observations = robot_model.sensor_readings

        # states = all possible locations
        self.states = []
        for i in range(0, robot_model.maze.width * robot_model.maze.height):
            self.states.append(i)

        # initial probability = 100% at starting location
        self.i_prob = [0] * 16
        startloc = robot_model.startloc[1] * robot_model.maze.width + robot_model.startloc[0]
        self.i_prob[startloc] = 1

        # transition probabilities = probability of getting from each state to another
        self.t_prob = self.get_t_prob()

        # emission probabilities = probability of getting scanning each color at each state
        self.e_prob = self.get_e_prob()

        # viterbi
        self.viterbi = Viterbi(self.observations, self.states, self.i_prob, self.t_prob, self.e_prob)

    def get_t_prob(self):
        """
        helper function to represent emission probabilities
        in the form of a 2-d array where index pairs represent state to state
        and array content represents probability of going s1 to s2
        :return:
        """
        t_prob = []

        # loop through each state-state pair
        for i in range(0, len(self.states)):
            state_probs = [0] * 16
            counter = 0
            for j in range(0, len(self.states)):

                # only non-zero probability if neither is floor
                if self.maze.is_floor_index(i) and self.maze.is_floor_index(j):

                    # check n/s/e/w
                    if j == i + self.maze.width or j == i - self.maze.width or j == i + 1 or j == i - 1:
                        state_probs[j] = 0.25
                        counter += 1

                    # probability of staying still is 1 minus probability of moving
                    state_probs[i] = 1 - 0.25 * counter

            t_prob.append(state_probs)
        return t_prob

    def get_e_prob(self):
        """
        helper function to represent emission probabilities
        in the form of a 2-d array where the first index represents state
        and the second index represents colors rgby
        :return:
        """
        e_prob = []
        colors = ["R", "G", "B", "Y"]

        # loop through each state-color pair
        for loc in self.states:
            color_probs = [0] * 4
            true_color = self.maze.get_color_index(loc)

            # can't be any color if it's a wall
            if true_color != "#":

                # for each color, more likely if matches
                for i in range(0, 4):
                    if colors[i] == true_color:
                        color_probs[i] = 0.88
                    else:
                        color_probs[i] = 0.04

            e_prob.append(color_probs)

        return e_prob

    def solve(self):
        """
        solve! runs viterbi
        :return:
        """
        # convert path to list of coordinates
        indices_path = self.viterbi.viterbi()
        path = []
        for i in indices_path:
            x = i % self.maze.width
            y = i // self.maze.width
            path.append([x, y])

        mistakes = 0
        rand_mistakes = 0

        print("at each time step:")
        print("location\t\tprediction")
        print("---\t\t\t\t---")

        # print each step
        for i in range(0, len(self.actual_path)):
            location = self.actual_path[i]
            prediction = path[i]
            rand = self.random_path[i]

            # mistake if incorrect prediction
            if location != prediction:
                mistakes += 1

            if location != rand:
                rand_mistakes += 1

            print(str(self.actual_path[i]) + "\t\t\t" + str(prediction) + "\t\t\t" + str(rand))

        print()
        print(mistakes, "mistakes")
        print(rand_mistakes, "mistakes with random walk")


# bit of test code
if __name__ == "__main__":
    maze1 = Maze("mazes/maze3.maz")
    test_robot = RobotModel(maze1)
    walk = RandomWalk(maze1)

    vs = ViterbiSolver(test_robot, walk)
    vs.solve()
