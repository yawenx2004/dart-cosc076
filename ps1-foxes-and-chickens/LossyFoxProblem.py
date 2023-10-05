# author: @yawen_xue; scaffolding by cs76 faculty
# date: 18 sep. 23
# purpose: cs76 lab fox problem class

class LossyFoxProblem:
    def __init__(self, start_state=(3, 3, 1, 0), e=2):
        self.start_state = start_state
        self.goal_state = (0, 0, 0, 0)
        self.e = e
        self.num_chickens = start_state[0]
        self.num_foxes = start_state[1]
        self.chickens_lost = start_state[3] # not a constant
        self.found = False # not a constant

    # helper function to return number of chickens lost in each case
    # based on is_legal() in original FoxProblem.py
    def num_lost(self, state):

        # return 0 if illegal, 1 if legal without chicken loss, 2 if legal with chicken loss
        # illegal if there's a negative number of chickens or foxes on either side
        if state[0] < 0 or state[1] < 0 or state[1] > self.num_foxes:
            return -1
        elif state[0] > self.num_chickens - state[3]:
            return -1

        # also illegal if chicken loss exceeds e
        if state[3] > self.e:
            return -1

        # always legal and also no chickens lost if 0 chickens on either side
        if state[0] == 0 or state[0] == self.num_chickens:
            return 0

        # all chickens lost if number of foxes greater than number of chickens on left shore
        elif state[0] < state[1]:
            num_lost = state[0]
            return num_lost

        # same thing on right shore
        elif self.num_chickens - state[3] - state[0] < self.num_foxes - state[1]:
            num_lost = self.num_chickens - state[3] - state[0]
            return num_lost

        return 0

    # helper function to make sure that the number of chickens lost does not exceed e
    def enough_chickens_left(self, state, num_lost):

        # there are enough chickens left if loss of chicken plus additional lost of chickens does not exceed e
        #  so the state is legal
        if self.chickens_lost + num_lost <= self.e:
            return True

        return False

    # helper function to append state to list of successors, if said state is legal
    def add_successor(self, state, successors_list):
        x = self.num_lost(state)

        # we do not want illegal states!!!
        if x == -1:
            return None

        # if state is legal and does not result in loss of chickens, add to successors_list
        if x == 0:
            successors_list.append(state)

        # if there is a positive number of chickens lost... change state,
        #  check legality using enough_chickens_left, and add
        else:
            if self.enough_chickens_left(state, x):

                # if on left shore
                if state[2] == 0:

                    # if we have too much chicken loss, break; else add to list
                    if state[3] + x > self.e:
                        return None
                    successors_list.append((0, state[1], 0, state[3] + x))

                # right shore
                if state[2] == 1:

                    # if we have too much chicken loss, break; else add to list
                    if state[3] + x > self.e:
                        return None
                    successors_list.append((0, state[1], 1, state[3] + x))

        return successors_list

    # get successor states for the given state
    def get_successors(self, state):

        # changed this to set to avoid redundancy
        successors = []

        # if boat is on left shore
        if state[2] == 1:

            # 2 chickens, 1 chicken, 2 foxes, 1 fox, 1 chicken 1 fox
            self.add_successor((state[0]-2, state[1], 0, state[3]), successors)
            self.add_successor((state[0]-1, state[1], 0, state[3]), successors)
            self.add_successor((state[0], state[1]-2, 0, state[3]), successors)
            self.add_successor((state[0], state[1]-1, 0, state[3]), successors)
            self.add_successor((state[0]-1, state[1]-1, 0, state[3]), successors)

        # if boat is on right shore
        elif state[2] == 0:

            # 2 chickens, 1 chicken, 2 foxes, 1 fox, 1 chicken 1 fox
            self.add_successor((state[0]+2, state[1], 1, state[3]), successors)
            self.add_successor((state[0]+1, state[1], 1, state[3]), successors)
            self.add_successor((state[0], state[1]+2, 1, state[3]), successors)
            self.add_successor((state[0], state[1]+1, 1, state[3]), successors)
            self.add_successor((state[0]+1, state[1]+1, 1, state[3]), successors)
        return successors

    # returns true if we've reached the goal
    def goal_test(self, state):
        if state[0] == self.goal_state[0] and state[1] == self.goal_state[1] and state[2] == self.goal_state[2]:
            return True
        else:
            return False

    def __str__(self):
        string =  "Foxes and chickens problem: " + str(self.start_state)
        return string

# a bit of test.py code
if __name__ == "__main__":
    test_cp = LossyFoxProblem((3, 3, 1, 0), e=3)
    print(test_cp.get_successors((2, 2, 0, 1)))
    print(test_cp)
