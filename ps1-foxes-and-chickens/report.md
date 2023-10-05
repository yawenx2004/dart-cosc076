Yawen Xue\
COGS 44\
PS1 - Foxes and Chickens\
17 Sep. 23
## Introduction
The upper bound for the number of states is 4×4×2=32. There are 3 possible states for the number of chickens (0-3), 3 for the number of foxes (0-3 again), and 2 for the location of the boat (0-1; left/right).

Here is my graph of states, beginning from (3, 3, 1). Illegal states are marked in red, while repeating states are marked in yellow.

_See Figure 1._
## Code Design
### FoxProblem.py
In this section, I worked on four methods within the scaffold -- I filled out get_successors() (and wrote two additional helper functions, add_successor() and is_legal()) and goal_test. In get_successors(), I used addition and subtraction as a means to reach all possible states (legal or illegal) based on the position of the boat (0 or 1). That is, +- two chickens, +- one chicken, +- two foxes, +- one fox, +- one chicken, one fox. I used add_successor() as a helper function to add a state to the list output of get_successors(), after using is_legal() as an additional helper function to check if the state is legal (that is, more foxes than chickens on either side (unless the number of chickens is zero), or a negative number of foxes or chickens on either side). The method goal_test() returns true when the state reached is equivalent to the given goal (usually (0, 0, 0)).
### BFS
I referred to the pseudocode given to us when implementing BFS. I created a deque of frontiers to explore and a backpointers dictionary that helps with backchaining when the time comes to retrieve the path. While the frontier is not empty and the goal has not been reached, I looped through the frontier in a FIFO order (all the while adding new frontiers from the adjacency lists of explored nodes). I marked visited states to keep track of them and used the dictionary to link each state to the state we visited it from.
### DFS
For DFS, I wrote a recursive function, base case being that the current node contains the goal state. Until the base case is reached, the function recurses. In the recursive state, we first loop through successors and check each node to make sure it's not in solution.path (hence the path-checking). If this is true, the function recurses with the new solution (and therefore its path) as a parameter.

Q. Does memoizing dfs save significant memory with respect to breadth-first search? Why or why not?

Memoizing DFS can save significant memory compared to BFS. BFS keeps both a frontier (list of future nodes
to explore) and a set of visited points. The frontier can grow very very long as we go deeper into the graph. Memoized DFS, on the other hand, stores a table of previously-found solutions, thereby avoiding the need to operate on loops and redundant paths.

Q. Does path-checking depth-first search save significant memory with respect to breadth-first search? Draw an example of a graph where path-checking dfs takes much more run-time than breadth-first search; include in your report and discuss.

Path-checking DFS can save significant memory compared to BFS. While BFS needs to keep track of nodes to visit (a list that can grow exponentially), path-tracking DFS uses recursion and only needs to keep track of nodes along a single path. However, path-checking DFS does not necessarily save memory as compared to BFS. For example, in graphs where the goal node is relatively shallow in the architecture of the graph, but not located along the first path deep into the graph. For example, below I have drawn a figure where BFS would find the goal node, G, very quickly, since it would be among the first nodes to be added to the algorithm's frontier queue. On the other hand, path-checking DFS would first need to explore a couple of paths that go on very deep into the graph, and only then would it reach node G.

_See Figure 2._
### IDS
In my IDS implementation, I looped DFS with a depth limit of 1 within a while loop that operates until iterations reaches the maximum number.

Q. On a graph, would it make sense to use path-checking dfs, or would you prefer memoizing dfs in your iterative deepening search? Consider both time and memory aspects. (Hint. If it’s not better than bfs, just use bfs.)

Path-checking DFS has the advantage of using less memory as it doesn't need to keep a memoization table, but it can have high runtime cost when it comes to graphs with greater height (that is, depth). Memoizing DFS uses more memory, but it can be faster when it comes to graphs with greater height, as it avoids redundancy more effectively. Given any graph, if I have no information about its depth, I'd prefer memoizing DFS, as it can be implemented in such a way that it generates the optimal solution. It also generally uses less memory than BFS and is faster.
### Lossy Chickens and Foxes
Given a round of the chicken-and-foxes problem where no more than E chickens could be eaten, four states (that is, one additional state) would be necessary -- one to denote the number of chickens, one to denote the number of foxes, one to denote the position of the boats, and one to denote the number of chickens that have been eaten.

To accomodate this change, in my FoxProblem.py file I'd make changes to the is_legal() function. While currently a move is illegal if the number of foxes exceeds the number of chickens on either side, in my new function I'd set this case as legal, but change the state sequence so that the fourth state -- tne number of chickens eaten -- increments by one whenever this happens. Then, is_legal() would deem a move illegal if it results in the fourth state exceeding the given E constant.
## Extension
### Lossy Chickens and Foxes
I implemented LossyFoxProblem.py and tested it with lossy_foxes.py. Note that due to the structure of my BFS function in uninformed_search.py, I cannot accurately run BFS on LossyFoxProblem as my BFS makes use of a goal state in backchaining and LossyFoxProblem has more than one possible goal states. So unless E equals 0, the BFS result is not guaranteed to be optimal. DFS and IDS, however, remain useful.

Implemeting this has involved a lot more changes than expected from what I discussed in the previous function — I altered the is_legal() function, as predicted, but I further changed it into num_lost so that it returns the number of chickens lost from each state transition (or -1 if the move is illegal). I also added a enough_chickens_left() function as a further legality check, to prevent states in which chicken loss exceeds E. My add_successors() function also involves more step to fully test the legality of each state.
### Memoizing DFS
I also implemented memoizing DFS in uninformed_search.py. Here, instead of recursion, I used a stack (LIFO) to keep track of nodes and a visited set to memoize. While the stack is not empty, I loop through successors and check for solutions.
