# author: @yawen_xue
# date: 12 nov. 23
# purpose: testing rrt

from BONUS_RRT import RRT
from BONUS_RRT2 import RRT2
from BONUS_RRTControl import RRTControl

robot = (0, 0)
goal = (100, 0)
env0 = (100, 100, [])
env1 = (100, 100, [[(30, -10), (30, 20), (35, 20), (35, -10)]])
env2 = (100, 100, [[(30, -10), (30, 60), (35, 60), (35, -10)]])
env3 = (100, 100, [[(30, -10), (30, 60), (35, 60), (35, -10)],
                   [(30, 80), (30, 110), (35, 110), (35, 80)],
                   [(70, 110), (70, 50), (75, 50), (75, 110)],
                   [(60, 0), (60, 40), (80, 40), (80, 0)]])
env4 = (100, 100, [[(10, -10), (10, 60), (15, 60), (15, -10)],
                   [(30, -10), (30, 60), (35, 60), (35, -10)],
                   [(20, 30), (20, 110), (25, 110), (25, 30)],
                   [(70, 110), (70, 50), (75, 50), (75, 110)],
                   [(60, 0), (60, 40), (80, 40), (80, 0)]])

'''change third parameter to change environment'''
rrt = RRT(robot, goal, env1)
rrt2 = RRT2(robot, goal, env1)
control = RRTControl(robot, goal, env4)

'''comment in/out to test'''
# rrt.visualize_env()
# rrt.grow_tree_vis(step_by_step=True)
rrt.solve(visualize=True)

# rrt2.visualize_env()
# rrt2.grow_tree_vis(step_by_step=True)
rrt2.solve(visualize=True)

# control.grow_tree_vis(step_by_step=True)
# control.solve()

