# author: @yawen_xue; scaffolding by cs76 faculty
# date: 18 sep. 23
# purpose: cs76 lab a* search class

from SearchSolution import SearchSolution
from heapq import heappush, heappop

class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        self.state = state
        self.heuristic = heuristic              # h(n)
        self.parent = parent
        self.transition_cost = transition_cost  # g(n)

    def priority(self):
        # f(n) = h(n) + g(n)
        return self.heuristic + self.transition_cost

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result

def astar_search(search_problem, heuristic_fn):
    # I'll get you started:
    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    pqueue = []
    heappush(pqueue, start_node)

    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    visited_cost = {}
    visited_cost[start_node.state] = 0

    # you write the rest:
    # while priority queue is not empty, continue to construct path
    while pqueue:

        # get node with lowest priority
        curr_node = heappop(pqueue)
        solution.nodes_visited += 1

        # if we've reached goal, return path
        if search_problem.goal_test(curr_node.state):
            solution.path = backchain(curr_node)
            solution.cost = curr_node.transition_cost
            return solution

        # mark node as visited
        visited_cost[curr_node.state] = curr_node.transition_cost

        # loop through successors
        for next_state in search_problem.get_successors(curr_node.state):

            # calculate next transition cost
            next_transition_cost = curr_node.transition_cost + search_problem.get_transition_cost(next_state, curr_node.state)
            next_node = AstarNode(next_state, heuristic_fn(next_state), parent=curr_node, transition_cost=next_transition_cost)

            # if state hasn't been visit, visit it
            if next_state not in visited_cost or next_transition_cost < visited_cost[next_state]:
                heappush(pqueue, next_node)
                visited_cost[next_state] = next_transition_cost

    return solution