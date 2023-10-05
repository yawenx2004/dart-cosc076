# author: @yawen_xue; scaffolding by cs76 faculty
# date: 13 sep. 23
# purpose: cs76 lab 1 search implementations

from collections import deque
from SearchSolution import SearchSolution

# you might find a SearchNode class useful to wrap state objects,
#  keep track of current depth for the dfs, and point to parent nodes
class SearchNode:

    # each search node except the root has a parent node
    #  and all search nodes wrap a state object
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

# you might write other helper functions, too. For example,
# I like to separate out backchaining, and the dfs path checking functions

def bfs_search(search_problem):

    # initiate search frontier and backpointers
    solution = SearchSolution(search_problem, "BFS")
    path = []
    frontier = deque()
    frontier.append(search_problem.start_state)
    visited_from = {search_problem.start_state: None}

    # while frontier not empty and goal not reached
    while len(frontier) != 0 and search_problem.goal_state not in visited_from:

        # retrieve state to visit in FIFO order
        curr_state = frontier.popleft()
        solution.nodes_visited += 1

        # for each state in the current state's adjacency list
        #  if state has yet been visited, add to search frontier
        adj_list = search_problem.get_successors(curr_state)
        for next_state in adj_list:
            if next_state not in visited_from:
                visited_from[next_state] = curr_state
                frontier.append(next_state)

    # return path
    path_point = search_problem.goal_state
    if path_point not in visited_from:
        return solution

    while path_point != None:
        path.append(path_point)
        path_point = visited_from[path_point]

    # reverse path; add path to solution
    solution.path = path[::-1]
    return solution

# Don't forget that your dfs function should be recursive and do path checking,
#  rather than memoizing (no visited set!) to be memory efficient

# We pass the solution along to each new recursive call to dfs_search
#  so that statistics like number of nodes visited or recursion depth
#  might be recorded
def dfs_search(search_problem, depth_limit=100, node=None, solution=None):

    # if no node object given, create a new search from starting state
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")

    # you write this part
    solution.path.append(node.state)
    solution.nodes_visited += 1

    # base case: current node is the goal
    if search_problem.goal_test(node.state):
        search_problem.found = True
        return solution

    # another base case: depth limit reached
    if depth_limit == 0:
        return solution

    # recursive case
    # loop through successors; run dfs if successor not in solution path
    for successor in search_problem.get_successors(node.state):
        if successor not in solution.path and depth_limit > 0:
            new_solution = dfs_search(search_problem, depth_limit=depth_limit-1, node=SearchNode(successor, node), solution=solution)
            if search_problem.found:
                return new_solution

            # remove children without solutions
            else:
                if solution.path:
                    solution.path.pop()

    # no solution found
    if len(solution.path) == 1:
        solution.path = []
    return solution

def ids_search(search_problem, depth_limit=100):

    # you write this part
    solution = SearchSolution(search_problem, "DFS")
    i = 1
    while i < depth_limit:

        # reset whether or not problem has been solved
        search_problem.found = False
        solution = dfs_search(search_problem, depth_limit=i)

        # if problem has been solved, break
        if search_problem.found:
            solution.search_method = "IDS"
            return solution
        i += 1

    # if no solution found
    solution.search_method = "IDS"
    return solution


def memoizing_dfs_search(search_problem, depth_limit=100, node=None, solution=None):

    # create node & initialize things
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "MDFS")
        search_problem.found = False
    visited = set()
    stack = [(node, solution, depth_limit)]

    while stack:
        node, solution, depth_limit = stack.pop()
        solution.path.append(node.state)
        solution.nodes_visited += 1

        # if current node is goal, return solution
        if search_problem.goal_test(node.state):
            search_problem.found = True

            # get rid of paths that lead nowhere
            solution.path.pop()
            return solution

        # depth limit reached, return solution
        if depth_limit == 0:
            return solution

        # loop through successors
        successors = search_problem.get_successors(node.state)
        unvisited = [s for s in successors if s not in visited]
        for successor in unvisited:
            visited.add(successor)
            successor_node = SearchNode(successor, node)
            stack.append((successor_node, solution, depth_limit - 1))

    # no solution found
    if len(solution.path) == 1 or solution.path[-1] != search_problem.goal_state:
        solution.path = []
    return solution