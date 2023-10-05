# author: @yawen_xue; scaffolding by cs76 faculty
# date: 24 sep. 23
# purpose: cs76 lab sensorless problem testing

# You write this:
from SensorlessProblem import SensorlessProblem
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

test_mp = SensorlessProblem(test_maze3)
test_mp2 = SensorlessProblem(test_maze2)
test_mp4 = SensorlessProblem(test_maze4)
test_mp5 = SensorlessProblem(test_maze5)
test_mp6 = SensorlessProblem(test_maze6)
test_mp7 = SensorlessProblem(test_maze7)

#print(test_mp.get_successors(test_mp.start_state))

# this should explore a lot of nodes; it's just uniform-cost search
result = astar_search(test_mp, null_heuristic)
print(result)
#test_mp.animate_path(result.path)

# this should do a bit better:
result = astar_search(test_mp, test_mp.eliminate_four)
print(result)

result = astar_search(test_mp, test_mp.halve_successors)
print(result)

# Your additional tests here:
# 5x6 mazes
print(astar_search(test_mp2, null_heuristic))
print(astar_search(test_mp2, test_mp2.eliminate_four))
print(astar_search(test_mp2, test_mp2.halve_successors))

print(astar_search(test_mp4, null_heuristic))
print(astar_search(test_mp4, test_mp4.eliminate_four))
print(astar_search(test_mp4, test_mp4.halve_successors))

print(astar_search(test_mp5, null_heuristic))
print(astar_search(test_mp5, test_mp5.eliminate_four))
print(astar_search(test_mp5, test_mp5.halve_successors))

print(astar_search(test_mp6, null_heuristic))
print(astar_search(test_mp6, test_mp6.eliminate_four))
print(astar_search(test_mp6, test_mp6.halve_successors))

# 10x12 maze
#print(astar_search(test_mp7, null_heuristic)
print(astar_search(test_mp7, test_mp7.eliminate_four))
#print(astar_search(test_mp7, test_mp7.halve_successors))