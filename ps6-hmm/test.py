# author: @yawen_xue
# date: 4 nov. 23
# purpose: testing my code!! :)

from Maze import Maze
from RobotModel import RobotModel
from HMM import HMM

from BONUS_RandomWalk import RandomWalk
from BONUS_Viterbi import ViterbiSolver
from BONUS_ForwardBackward import ForwardBackwardSolver

maze1 = Maze("mazes/maze1.maz")
maze2 = Maze("mazes/maze2.maz")
maze3 = Maze("mazes/maze3.maz")

'''change this to change mazes'''
maze = maze3

test_robot = RobotModel(maze)
walk = RandomWalk(maze)
hmm = HMM(test_robot, walk)
vs = ViterbiSolver(test_robot, walk)
fbs = ForwardBackwardSolver(test_robot, walk)


def test_hmm():
    print("testing HMM:")
    hmm.solve()


def test_viterbi():
    print("testing Viterbi:")
    vs.solve()


def test_forward_backward():
    print("testing forward-backward:")
    fbs.solve()


'''comment in to run'''
# test_hmm()
# test_viterbi()
test_forward_backward()
