# author: @yawen_xue; scaffolding by cs76 faculty
# date: 21 sep. 23
# purpose: cs76 lab mazeworld problem class

from Maze import Maze
from time import sleep

class SensorlessProblem:

    ## You write the good stuff here:
    def __init__(self, maze):
        self.maze = maze
        self.start_state = tuple(self.all_belief_states())

    # collects a set of all belief states, for start state
    def all_belief_states(self):
        all_belief_states_list = []

        # belief states initially includes all valid square within the map
        for x in range(0, self.maze.width):
            for y in range(0, self.maze.height):
                if self.maze.is_floor(x, y):
                    all_belief_states_list.append(x)
                    all_belief_states_list.append(y)

        return all_belief_states_list

    def __str__(self):
        string =  "Blind robot problem: "
        return string

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def get_successors(self, state):
        successors = []

        # north, south, east, west; narrow down location by checking if movement in that direction is possible
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        for direction in directions:
            self.edit_successors(successors, state, direction[0], direction[1])

        return successors

    # helper function for get_successors() that edits to reflect new knowledge following actions
    def edit_successors(self, successors, state, dx, dy):
        visited = set()
        edited_successors = []

        # loop through states
        for i in range(0, len(state)-1):
            if i % 2 == 0:
                belief = [state[i], state[i+1]]

                # get new state after moving in given direction
                next_belief = belief.copy()
                next_belief[0] += dx
                next_belief[1] += dy

                # if robot can go there, we add to belief state
                if self.maze.is_floor(next_belief[0], next_belief[1]):
                    edited_successors.append(next_belief[0])
                    edited_successors.append(next_belief[1])
                    visited.add(tuple(next_belief))

                # also, unvisited states remain in belief list
                elif tuple(belief) not in visited:
                    edited_successors.append(belief[0])
                    edited_successors.append(belief[1])
                    visited.add(tuple(belief))

        # append to successors list if not empty
        if len(edited_successors) != 0:
            successors.append(tuple(edited_successors))

    # helper function to recognize when search function reaches the goal
    def goal_test(self, curr_belief_states):
        # we've reached the goal if length of belief states is 1 square and therefore we know where we are
        if len(curr_belief_states) == 2:
            return True

        return False

    # heuristic function, in which we assume that each iteration of get_successors() rules out moves in all cardinal directions
    def eliminate_four(self, successors):
        return len(successors) - 4

    # another heuristic function, assuming we halve number of belief states with every iteration
    def halve_successors(self, successors):
        return len(successors)/2

    # helper function to calculate transition cost for search function
    def get_transition_cost(self, next_state, curr_state):
        return 1

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state)
            sleep(1)

            print(str(self.maze))


## A bit of test.py code
if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_problem = SensorlessProblem(test_maze3)
    #print(test_maze3)
    #print(test_problem.start_state)
    print(test_problem.get_successors((0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 1, 0, 1, 1, 1, 2, 1, 3, 1, 4),))