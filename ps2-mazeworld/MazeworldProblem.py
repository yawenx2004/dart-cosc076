# author: @yawen_xue; scaffolding by cs76 faculty
# date: 19 sep. 23
# purpose: cs76 lab mazeworld problem class

from Maze import Maze
from time import sleep

class MazeworldProblem:
    ## you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations):
        self.maze = maze
        self.goal_locations = goal_locations
        self.start_state = tuple([0] + maze.robotloc)
        self.num_robots = len(maze.robotloc)/2

    def __str__(self):
        string =  "Mazeworld problem: "
        return string

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    # return neighboring nodes for a* search
    def get_successors(self, state):
        successors = []

        # determine indices of state to change
        ix = 2 * state[0] + 1    # x-coordinate of state[0]-th robot
        iy = 2 * state[0] + 2    # y-coordinate of state[0]-th robot

        # build potential successor list from cardinal directions
        #  then check legality
        n = list(state)         # concert to list b/c tuples are immutable
        n[iy] += 1
        s = list(state)
        s[iy] -= 1
        e = list(state)
        e[ix] += 1
        w = list(state)
        w[ix] -= 1
        successors += [n, s, e, w]
        successors = self.filter_successors(successors, ix, iy)

        # staying in place and moving on to the next robot is always a legal choice
        stay_put = list(state)
        stay_put[0] = int((s[0] + 1) % self.num_robots)
        stay_put = tuple(stay_put)

        return successors + [stay_put]

    # helper function for get_successors()
    #  filters a list of candidates
    def filter_successors(self, successors, ix, iy):
        filtered_successors = []

        for s in successors:
            x = s[ix]
            y = s[iy]

            # legal if (x, y) is part of the floor space
            if self.maze.is_floor(x, y):

                # check that space is not already occupied by another robot
                if not self.is_collision(s, ix, iy):

                    # increment state[0] in preparation for new robot
                    s[0] = int((s[0] + 1) % self.num_robots)

                    # convert back to tuple
                    filtered_successors.append(tuple(s))

        return filtered_successors

    # helper function to prevent collisions
    def is_collision(self, successor, ix, iy):
        x = successor[ix]
        y = successor[iy]

        # make list of locations of other robots (the ones not being currently acted on)
        robot_loc = successor[1:ix] + successor[iy+1:]

        #  basically has_robot() from maze.py but doesn't need an updated maze object first
        for i in range(0, len(robot_loc), 2):
            rx = robot_loc[i]
            ry = robot_loc[i + 1]
            if rx == x and ry == y:
                return True

        return False

    # helper function to recognize when search function reaches the goal
    def goal_test(self, state):
        # we remove state[0] to get current location
        if state[1:] == self.goal_locations:
            return True

        return False

    # helper function for manhattan distance heuristic
    def manhattan_heuristic(self, state):
        mdist = 0
        state = state[1:]   # state is one element longer than goal_locations

        # absolute value of difference between x- and y-coordinates of current state and goal
        for i in range(len(self.goal_locations)):
            mdist += abs(self.goal_locations[i] - state[i])

        return mdist

    # helper function to calculate transition cost for search function
    def get_transition_cost(self, next_state, curr_state):
        # return 1 if robot has moved (if it moves it can only move one square)
        if next_state[1:] != curr_state[1:]:
            return 1

        # return 0 if robot is staying put
        return 0

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[1:])
            sleep(1)

            print(str(self.maze))


## A bit of test.py code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

    print(test_mp.get_successors((1, 1, 1, 2, 1, 3, 1, 4)))

