# author: @yawen_xue
# date: 11 nov. 23
# purpose: testing prm

from ArmRobot import ArmRobot
from PRM import PRM
from BFSSolver import BFSSolver

# 2r robot
r2 = ArmRobot(2, [85, 0])
obstacles2 = [[(1, 1), (1, 1.25), (1.25, 1.25)], [(0.5, 1), (0.5, 1.5), (1, 1.5), (1, 1)], [(-0.5, -0.5), (-0.5, -1), (-1, -1)]]
prm2 = PRM(r2, [200, 350], obstacles2, k=100, num_samples=200)
bs2 = BFSSolver(r2, prm2)

# 4r robot
r4 = ArmRobot(4, [0, 0, 0, 300])
obstacles4 = [[(-1, -0.25), (-1, 1.5), (-1.5, 1.5)], [(2, 1.75), (2, 2.25), (1.5, 2.25), (1.5, 1.75)], [(-0.5, -0.5), (-0.5, -1), (-1, -1)]]
obstacles4xx = [[(-1, 1), (-1, 1.5), (-1.5, 1.5)], [(2, 1.75), (2, 2.25), (1.5, 2.25), (1.5, 1.75)], [(-0.5, -0.5), (-0.5, -1), (-1, -1)]]

prm4 = PRM(r4, [120, 330, 0, 0], obstacles4, k=100, num_samples=200)        # easy
prm4x = PRM(r4, [120, 330, 90, 75], obstacles4, k=100, num_samples=200)     # harder
prm4xx = PRM(r4, [210, 330, 90, 75], obstacles4xx, k=100, num_samples=200)  # hardest

''' select which 4r problem here '''
# bs4 = BFSSolver(r4, prm4)
# bs4 = BFSSolver(r4, prm4x)
bs4 = BFSSolver(r4, prm4x)

# testing!
'''possible configurations for 2r robot'''
# prm2.get_roadmap()
# prm2.visualize_configs()
# prm2.visualize_samples()

'''solution for 2r robot'''
# bs2.solve()

'''possible configurations for 4r robot'''
# prm4.get_roadmap()
# prm4.visualize_configs()

'''solution for 4r robot'''
bs4.solve()
