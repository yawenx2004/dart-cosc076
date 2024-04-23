# @author: yawen_x
# date: 11 nov. 23, updated 22 apr. 24
# purpose: test prm!

from ArmRobot import ArmRobot
from PRM import PRM
from PRMSolver import PRMSolver

''' here are test cases i've written for you: an 2r robot and a 4r robot with varying levels of difficulty'''
r2 = ArmRobot(2, [85, 0])
obstacles2 = [[(1, 1), (1, 1.25), (1.25, 1.25)],
              [(0.5, 1), (0.5, 1.5), (1, 1.5), (1, 1)],
              [(-0.5, -0.5), (-0.5, -1), (-1, -1)]]
prm2 = PRM(r2, [200, 350], obstacles2, k=100, num_samples=200)
s2 = PRMSolver(r2, prm2)

r4 = ArmRobot(4, [0, 0, 0, 300])
obstacles4 = [[(-1, -0.25), (-1, 1.5), (-1.5, 1.5)],
              [(2, 1.75), (2, 2.25), (1.5, 2.25), (1.5, 1.75)],
              [(-0.5, -0.5), (-0.5, -1), (-1, -1)]]
obstacles4xx = [[(-1, 1), (-1, 1.5), (-1.5, 1.5)],
                [(2, 1.75), (2, 2.25), (1.5, 2.25), (1.5, 1.75)],
                [(-0.5, -0.5), (-0.5, -1), (-1, -1)]]
prm4 = PRM(r4, [120, 330, 0, 0], obstacles4, k=100, num_samples=200)        # easy
prm4x = PRM(r4, [120, 330, 90, 75], obstacles4, k=100, num_samples=200)     # harder
prm4xx = PRM(r4, [210, 330, 90, 75], obstacles4xx, k=100, num_samples=200)  # hardest

''' comment in to select which 4r problem you'd like to test '''
# s4 = PRMSolver(r4, prm4)
# s4 = PRMSolver(r4, prm4x)
s4 = PRMSolver(r4, prm4xx)

''' testing! '''
''' visualize possible configurations for 2r robot '''
# prm2.get_roadmap()
# prm2.visualize_configs()
# prm2.visualize_samples()

''' solve for 2r robot '''
# s2.solve()

''' visualize possible configurations for 4r robot '''
# prm4.get_roadmap()
# prm4.visualize_configs()

''' solve for 4r robot '''
s4.solve(visualize=True)
