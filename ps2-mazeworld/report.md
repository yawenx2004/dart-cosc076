Yawen Xue\
COGS 44\
PS2 - MazeWorld\
18 Sep. 23
# Code Design and Implementation
## MazeworldProblem.py
I wrote a get_successors() function to use in search algorithms. Since states are given in a tuple where the first element denotes the robot to move and the following pairs of elements denote robot locations, get_successors() uses state[0] to decide which robot to move -- and, subsequently, which x-y pair to change. The function loops through north, south, east, west, and staying put. The helper function filter_successors() filters through these states to determine which ones are legal -- that is, for which ones self.maze.is_floor() returns true, and which ones do not result in a collision. To check for collisions I have another helper function is_collision(), which is very similar to has_robot() from Maze.py but does not require updating the maze first. Thereby get_successors() returns a list of legal successors to a given state.\
\
In addition, I wrote manhattan_heuristic() to calculate the Manhattan distance and get_Transition_cost() to calculate transition cost.\
\
For multi-robot coordination, I made sure that my get_successors() function checks for collisions (see above). Moreover, I made sure that the robots take turn moving, and that they can skip a turn for the sake of optimality. When a robot skips a turn, the state remains the same except for state[0], which increments and indicates that it's the next robot's turn.
## SensorlessProblem.py
For the blind robot problem, since we have information about the maze and the direction the robot is going in but not the current location of the robot, I set the start state to all points within the maze for which is_floor() returns true. Then, I used a get_successors() function alongside an edit_successors() helper function. To get successors for A* search, we attempt to move the robot one step in a cardinal direction -- north, south, east, or west -- and check the legality of the move. If the move is legal, we add it to the new set of belief states. There are unvisited squares and they, too, remain in the new set of belief states, as we haven't yet ruled them out. Eventually, this process reduces the belief state down to a single set of coordinates, at which point goal_test() returns true.
## Heuristic
I used the Manhattan Distance as a heuristic for the mazeworld problem. I calculated this by finding the sum of the absolute values of the difference between x- and y-coordinates of the current state and the goal state.\
\
I tested two heuristics for the blind robot problem set, one of which reduces the length of the number of successors by 4 (for the 4 cardinal directions) and another which halves the length of the successors. The heuristic eliminate_four() works faster and goes through fewer nodes.
## astar_search.py
My A* search function loops through the priority queue as established by the code we've been given. Each loop, it pops the node with the lowest priority, and loops through its successors (see get_successors() function in Mazeworld.py) to get new nodes to explore. New nodes have their costs calculated and added to the dictionary visited_cost so that the priority queue works for them and can continue to pop nodes with the lowest priority. If the goal has been reached, we return a SearchSolution object containing the path and other information.
# Testing
## test_mazeworld.py
I used maze3.maz and maze2.maz provided. In addition, I wrote maze4.maz, maze5.maz, and maze6.maz to test with 4, 5, and 6 robots, respectively. The code began to show noticeable decline in speed starting with 5 robots, and the 6 robots case had a runtime of approximately 1 minute 44 seconds. I did not try adding more robots.\
\
The path returned by using the null heuristic is always shorter than or of equal length to the path returned by using the Manhattan distance heuristic. However, in all cases except maze2.maz (single robot) and maze7.maz (single robot, single possible path), the null heuristic path also checks significantly more nodes than the Manhattan distance heuristic does. For the two exceptions, they check an equal number of nodes.
## test_sensorless.py
I tested with maze 2 through 7. My null heuristic works slowest, followed by my halve_successors heuristic. My eliminate_four heuristic works the fastest, and is the only one that returns a result for the larger maze (maze7.maz) within a minute. Even then, there is a roughly 10-second delay between the display of this function's output and the previous function's output.
# Discussion Questions
**Q1.** If there are k robots, how would you represent the state of the system? Hint – how many numbers are needed to exactly reconstruct the locations of all the robots, if we somehow forgot where all of the robots were? Further hint. Do you need to know anything else to determine exactly what actions are available from this state?\
\
I'd use a tuple of size 2k+1 to represent the system. The first tuple represents which robot's turn it is to move, and the following pairs indicate coordinates.\
\
**Q2.** Give an upper bound on the number of states in the system, in terms of n and k.\
\
Assuming n is the size of the maze (that is, number of squares), upper bound is k*(n^k) -- there are k possibilities for which robot's turn it is to move, and n^k possibilities for the number of occupied coordinates. This is an overestimate as it's more rigorously (n^k)((n-1)^k)((n-2)^k)... and so on, as the possible square for each robot to occupy decrements by 1.\
\
**Q3.** Give a rough estimate on how many of these states represent collisions if the number of wall squares is w, and n is much larger than k.\
\
There are n-w floor spaces and k robots to occupy them. A collision occurs when two or more robots occupy the same space. Therefore my rough estimate is (C(k, 2))(n-w)+(C(k, 3))(n-w)+...+(C(k, k))(n-w).\
\
**Q4.** If there are not many walls, n is large (say 100x100), and several robots (say 10), do you expect a straightforwards breadth-first search on the state space to be computationally feasible for all start and goal pairs? Why or why not?\
\
No. BFS has high memory cost and in such a maze it would need to store way too many nodes.\
\
**Q5.** Describe a useful, monotonic heuristic function for this search space. Show that your heuristic is monotonic. See the textbook for a formal definition of monotonic.\
\
The Manhattan distance is a useful monotonic heuristic function. It always underestimates the cost -- the Manhattan distance is the shortest possible distance between two points if you're travelling only in cardinal directions, and as a result it underestimates the cost when you factor in walls that make shortest-distance travel impossible.\
\
It is monotonic because costs always increase or stay the same as you continue down the search path. h(n) is always less than or equal to g(n') + c(n, n') + h(n') -- that is, the difference between the Manhattan heuristic to a node and to its successor is less than or equal to the cost of going to the successor from the start plus the cost of going from the node to its successor. It therefore never overestimates the cost.\
\
**Q6.** Implement a model of the system and use A* search to find some paths. Test your program on mazes with between one and three robots, of sizes varying from 5x5 to 40x40. (You might want to randomly generate the 40x40 mazes.) I’ll leave it up to you to devise some cool examples – but give me at least five and describe why they are interesting. (For example, what if the robots were in some sort of corridor, in the “wrong” order, and had to do something tricky to reverse their order?)\
\
Here are some of my test cases:
- maze4.maz - maze6.maz -- 4-6 robots, tests runtime
- maze7.maz -- single path, and as predicted cost is the same regardless of which heuristic I test
- maze8.maz -- 20x20, robots must reverse order in corridor
- maze9.maz -- 40x40, lots of paths that almost connect but not quite; shows relatively higher number of nodes explored, as expected
- maze10.maz -- 40x40, similar to 9 but more straightforward path; as expected a lot fewer nodes are visited\

\
**Q7.** Describe why the 8-puzzle in the book is a special case of this problem. Is the heuristic function you chose a good one for the 8-puzzle?\
\
The 8-puzzle is basically a mazeworld problem in which there are no walls and only one spot is not occupied by a robot. This would require a lot of coordination. The Manhattan distance is still a good heuristic, because it's admissible and it's basically the same problem.\
\
**Q8.** The state space of the 8-puzzle is made of two disjoint sets. Describe how you would modify your program to prove this. (You do not have to implement this.)\
\
The two disjoint sets of the 8-puzzle state soace are reachable from states within a set, but not from states in the other set. Therefore, to prove this, I'd implement a 8-puzzle using my mazeworld program, and run it with the correct state space. Then, I'll mix and move some of the set elements and show that this would render the puzzle unsolvable.
# Literature Review
While testing my MazeworldProblem code with 4-robot, 5-robot, and 6-robot cases, I discovered that A* searches, even with heuristics, have very high runtime costs when it comes to multi-robot coordination, to the point where my implementation takes almost 2 minutes to run when there are 5 robots present. In the paper Finding Optimal Solutions to Cooperative Pathfinding Problems, Trevor Standley discusses efficient algorithms for such cooperative pathfinding problems.\
\
The paper describes this very same issue with using traditional A* -- computational complexity increases exponentially as the number of agents increases. To counter this, Standley introduces operator decomposition, a method for reducing the search algorithm's branching factor to reduce search complexity. In A* with OD, branching factor is reduced from 9^n to 9 while goal depth only increases to nt. A* with OD accomplishes this by dividing the state space into subproblems where each robot is considered individually.\
\
The paper also discusses the simple independence detection algorithm, which aims for optimality by partitioning agents into disjoint and exhaustive sets to ensure that no collisions occur. SID starts with independent path planning, and when conflicts arises, it resolves them by finding alternative paths. If no alternative path can be found for conflicting groups, these groups are merged together. The algorithm is iterated until there are no collisions and all paths have been found.\
\
The algorithm proposed in the paper is able to significantly reduce computational complexity for multi-agent cooperative pathfinding problems through breaking the state space into subproblems and resolving conflicts when they arise. This is a very useful algorithm in real-world scenarios of multi-agent cooperative pathfinding.\
\
Standley, T. 2010. Finding optimal solutions to cooperative pathfinding problems. In The Twenty-Fourth AAAI Conference on Artificial Intelligence (AAAI’10), 173–178.
