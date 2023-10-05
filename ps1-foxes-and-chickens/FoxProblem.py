# author: @yawen_xue; scaffolding by cs76 faculty
# date: 14 sep. 23
# purpose: cs76 lab fox problem class

class FoxProblem:
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        self.num_chickens = start_state[0]
        self.num_foxes = start_state[1]
        self.found = False

    # helper function to test.py if successor states are legal
    def is_legal(self, state):

        # illegal if either fox or chicken number is negative
        if state[0] < 0 or state[0] > self.num_chickens or state[1] < 0 or state[1] > self.num_foxes:
            return False

        # legal if 0 chickens on either side
        if state[0] == 0 or state[0] == self.num_chickens:
            return True

        # illegal if number of foxes is greater than the number of chickens on left shore
        elif state[0] < state[1]:
            return False

        # same but right shore
        elif self.num_chickens-state[0] < self.num_foxes-state[1]:
            return False
        else:
            return True

    # helper function to append state to list of successors, if said state is legal
    def add_successor(self, state, successors_list):
        if self.is_legal(state):
            successors_list.append(state)
        return successors_list

    # get successor states for the given state
    def get_successors(self, state):
        successors = []

        # if boat is on left shore
        if state[2] == 1:

            # 2 chickens, 1 chicken, 2 foxes, 1 fox, 1 chicken 1 fox
            self.add_successor((state[0]-2, state[1], 0), successors)
            self.add_successor((state[0]-1, state[1], 0), successors)
            self.add_successor((state[0], state[1]-2, 0), successors)
            self.add_successor((state[0], state[1]-1, 0), successors)
            self.add_successor((state[0]-1, state[1]-1, 0), successors)

        # if boat is on right shore
        elif state[2] == 0:

            # 2 chickens, 1 chicken, 2 foxes, 1 fox, 1 chicken 1 fox
            self.add_successor((state[0]+2, state[1], 1), successors)
            self.add_successor((state[0]+1, state[1], 1), successors)
            self.add_successor((state[0], state[1]+2, 1), successors)
            self.add_successor((state[0], state[1]+1, 1), successors)
            self.add_successor((state[0]+1, state[1]+1, 1), successors)
        return successors

    # returns true if we've reached the goal
    def goal_test(self, state):
        if state == self.goal_state:
            return True
        else:
            return False

    def __str__(self):
        string =  "Foxes and chickens problem: " + str(self.start_state)
        return string

# a bit of test.py code
if __name__ == "__main__":
    test_cp = FoxProblem((3, 3, 1))
    print(test_cp.get_successors((2, 2, 0)))
    print(test_cp)
