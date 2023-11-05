# author: @yawen_xue
# date: 3 nov. 23
# purpose: generalized forward-backward algorithm

from Maze import Maze
from RobotModel import RobotModel
from BONUS_RandomWalk import RandomWalk
from BONUS_Viterbi import ViterbiSolver


class ForwardBackward:
    def __init__(self, observations, states, i_prob, t_prob, e_prob):
        self.observations = observations
        self.states = states
        self.i_prob = i_prob    # initial probabilities
        self.t_prob = t_prob    # transition probabilities
        self.e_prob = e_prob    # emission probabilities

    def forward(self):
        """
        calculates probability of being in particular state at each time step
        given observations up to that time step
        :return:
        """
        alpha = [[0.0] * len(self.states) for _ in range(0, len(self.observations))]

        # for conversion
        color_to_index = {"R": 0, "G": 1, "B": 2, "Y": 3}

        # initialize
        for i in range(0, len(self.states)):
            alpha[0][i] = self.i_prob[i] * self.e_prob[i][color_to_index[self.observations[0]]]

        # recurse
        for o in range(1, len(self.observations)):
            for s1 in range(0, len(self.states)):
                alpha[o][s1] = sum(
                    alpha[o - 1][s2] *
                    self.t_prob[s2][s1] *
                    self.e_prob[s1][color_to_index[self.observations[o]]]
                    for s2 in range(len(self.states)))

        # end
        prob = sum(alpha[len(self.observations) - 1])
        return alpha, prob

    def backward(self):
        """
        calculates probability of observing rest of the sequence
        from particular state at each time step
        :return:
        """
        beta = [[0.0] * len(self.states) for _ in range(0, len(self.observations))]

        # for conversion
        color_to_index = {"R": 0, "G": 1, "B": 2, "Y": 3}

        # initialize
        for i in range(0, len(self.states)):
            beta[len(self.observations) - 1][i] = 1.0

        # recurse
        for o in range(len(self.observations) - 2, -1, -1):
            for s1 in range(len(self.states)):
                beta[o][s1] = sum(
                    self.t_prob[s1][s2] *
                    self.e_prob[s2][color_to_index[self.observations[o + 1]]] *
                    beta[o + 1][s2]
                    for s2 in range(0, len(self.states)))

        # end
        prob = sum(
            self.i_prob[s] *
            self.e_prob[s][color_to_index[self.observations[0]]] *
            beta[0][s]
            for s in range(0, len(self.states)))
        return beta, prob

    def forward_backward(self):
        """
        forward-backward algorithm
        :return:
        """
        alpha, a_prob = self.forward()
        beta, b_prob = self.backward()

        posteriors = [[0.0] * len(self.states) for _ in range(0, len(self.observations))]
        total_prob = a_prob

        for o in range(0, len(self.observations)):
            for s in range(len(self.states)):
                posteriors[o][s] = (alpha[o][s] * beta[o][s]) / total_prob

        path = []
        for i in range(0, len(posteriors)):
            max_prob = 0
            best_state = None

            for j in range(0, len(posteriors[i])):
                if posteriors[i][j] > max_prob:
                    max_prob = posteriors[i][j]
                    best_state = j

            path.append(best_state)
        return path

class ForwardBackwardSolver(ViterbiSolver):
    def __init__(self, robot_model, random_walk):
        super().__init__(robot_model, random_walk)
        self.fb = ForwardBackward(self.observations, self.states, self.i_prob, self.t_prob, self.e_prob)

    def solve(self):
        """
        solve! runs algorithm and displays results
        :return:
        """
        # represent path with coordinates
        indices_path = self.fb.forward_backward()
        path = []
        for loc in indices_path:
            x = loc % self.maze.width
            y = loc // self.maze.width
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

    fbs = ForwardBackwardSolver(test_robot, walk)
    fbs.solve()
