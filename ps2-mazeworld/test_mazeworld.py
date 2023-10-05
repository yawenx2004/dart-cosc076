# author: @yawen_xue; scaffolding by cs76 faculty
# date: 24 sep. 23
# purpose: cs76 lab mazeworld testing

from MazeworldProblem import MazeworldProblem
from Maze import Maze

from uninformed_search import bfs_search
from astar_search import astar_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0

# Test problems
test_maze3 = Maze("maze3.maz")
test_maze2 = Maze("maze2.maz")
test_maze4 = Maze("maze4.maz")
test_maze5 = Maze("maze5.maz")
test_maze6 = Maze("maze6.maz")
test_maze7 = Maze("maze7.maz")
test_maze8 = Maze("maze8.maz")
test_maze9 = Maze("maze9.maz")
test_maze10 = Maze("maze10.maz")

test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
test_mp2 = MazeworldProblem(test_maze2, (2, 2))
test_mp4 = MazeworldProblem(test_maze4, (1, 4, 1, 3, 1, 2, 1, 1))
test_mp5 = MazeworldProblem(test_maze5, (1, 4, 1, 3, 1, 2, 1, 1, 1, 0))
test_mp6 = MazeworldProblem(test_maze6, (1, 4, 1, 3, 1, 2, 1, 1, 1, 0, 2, 5))
test_mp7 = MazeworldProblem(test_maze7, (0, 3))
test_mp8 = MazeworldProblem(test_maze8, (8, 19, 8, 18))
test_mp9 = MazeworldProblem(test_maze9, (28, 39, 28, 38))
test_mp10 = MazeworldProblem(test_maze10, (28, 39, 28, 38))

print(test_mp.get_successors(test_mp.start_state))

# this should explore a lot of nodes; it's just uniform-cost search
result = astar_search(test_mp, null_heuristic)
print(result)

# this should do a bit better:
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
#test_mp.animate_path(result.path)

# Your additional tests here:
# small maze w/ 1 robot
print(astar_search(test_mp2, null_heuristic))
print(astar_search(test_mp2, test_mp2.manhattan_heuristic))

# 4 robots
print(astar_search(test_mp4, null_heuristic))
print(astar_search(test_mp4, test_mp4.manhattan_heuristic))
'''
# 5 robots
print(astar_search(test_mp5, null_heuristic))
print(astar_search(test_mp5, test_mp5.manhattan_heuristic))

# 6 robots -- this block of code takes 1 minute 44 seconds to run
print(astar_search(test_mp6, null_heuristic))
print(astar_search(test_mp6, test_mp6.manhattan_heuristic))
'''
# single path, 1 robot, 4x maze size
print(astar_search(test_mp7, null_heuristic))
print(astar_search(test_mp7, test_mp7.manhattan_heuristic))

# 20x20, tricky maneuver
result = astar_search(test_mp8, test_mp8.manhattan_heuristic)
print(result)
#test_mp8.animate_path(result.path)

# 40x40, many dead ends
result = astar_search(test_mp9, test_mp9.manhattan_heuristic)
print(result)

# 40x40, not many dead ends
result = astar_search(test_mp10, test_mp10.manhattan_heuristic)
print(result)