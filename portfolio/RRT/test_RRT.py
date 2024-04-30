# author: @yawen_x
# date: 12 nov. 23, updated 22 apr. 24
# purpose: test rrt!

from RRT import RRT
from RRT_unstuck import RRT_unstuck
from RRT_control import RRT_control

# test cases
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

'''change third parameter to change test environment'''
rrt = RRT(robot, goal, env1)
rrt_unstuck = RRT_unstuck(robot, goal, env4)
rrt_control = RRT_control(robot, goal, env0)

'''comment in/out to test'''
# rrt.grow_tree(step_by_step=True)
# rrt.solve(visualize=True)

# rrt_unstuck.grow_tree(step_by_step=True)
# rrt_unstuck.solve(visualize=True)

# rrt_control.grow_tree(step_by_step=True)
# rrt_control.solve()
