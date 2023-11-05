Yawen Xue\
COGS 44\
PS6 - HMM\
26 Oct. 23
# Intro
Let's first define how I index the coordinates in the maze. The bottom left corner is (0, 0), and with each rightward move the x-coordinate increments by 1, while with each upward move the y-coordinate increments by 1. Here's a layout of the maze as a coordinate. The number inside each square represents the index that corresponds to it in each state tuple.
<pre>
  |----|----|----|----|
3 | 12 | 13 | 14 | 15 |
  |----|----|----|----|
2 | 8  | 9  | 10 | 11 |
  |----|----|----|----|
1 | 4  | 5  | 6  | 7  |
  |----|----|----|----|
0 | 0  | 1  | 2  | 3  |
  |----|----|----|----|
    0    1    2    3
</pre>
So, if you want to convert a coordinate into an index within a tuple/list/vector, just sum the y-coordinate times 4 with the x-coordinate.
## Sensor Model
The functions color_sensor() and RobotModel.py is an implementation of my sensor model. They're described in more detail below (see ##RobotModel.py). Essentially, we randomly pick a move and then  deploy the color sensor. The color sensor generates a random probability.

- If the random probability falls at or below 0.88, we return the actual color.
- Else, we return a random uniform choice of the other colors.
- This yields the 88/4/4/4 distribution as outlined in the problem set instructions.

## State Transition Model
We know the robot's starting location. Given location at timestep 1, we can calculate the probability of the robot being in each location at the next timestep. This is the sum of the products of each previous location our desired location is reachable from and the probability of the robot taking that step from the previous location. We multiply by the probabilities given in the sensor model so that the state transition model could use this information to guess the location.
## Filtering Algorithm Implementation
See HMM.py. My filtering algorithm consists of a predict() function and an update() function.
# Code Design and Implementation
## Maze.py
I first created Maze.py, based upon the provided code from PS2 with a few modifications, to represent each maze. This class basically serves to package a maze into its robot location and its layout as a list of lists. Functions get_color(), is_floor(), and has_robot() help provide information about each given coordinate.
## RobotModel.py
This is essentially my sensor model. The class takes the following parameters:

- **maze**, as an instance of Maze.py as described above
- **observations**, as a list of tuples (movement, sensor reading, actual robot location); obtained through the observe() function

The observe() function randomly selects a direction north, south, east, or west, attempts to move the robot in that location, and reads the color using the sensor. It appends a tuple to self.observations each time it's run.\
\
To get the color, I have the function color_sensor(). This takes the actual color of the square as a parameter, randomly generates a probability, and according to that probability and the probability distribution given to us it picks a color. It has a 0.88 chance of returning the correct color, and 0.04 of returning each of three wrong colors.
## HMM.py
HMM.py takes a robot model instance as a parameter. Upon initialization it has the following variables:

- **maze**, which is the maze used in the provided robot model
- **sensor_readings** in the form of a list, again from the provided robot model
- **start_state**, which is a 16-tuple with the position of the start state set as 1 and everything else set as 0 (since on timestep 0 we are certain that the robot is on its starting location)
- **actual_path**, which we use for testing; the filtering algorithm has no access to this information
- **state**, which begins identical to start_state, is updated as the algorithm runs

I also had a variable sum_state to make sure the sum of probabilities is equal to 1.\
\
For my state transition model, the majority of the work is done in predict() and update(). Here's a rundown of their functionality:

**predict()**

- we start with a new, blank state where every probability is set to 0
- we loop through every location in the current state, and focus on the ones with non-zero probability, since each location is only reachable from itself or from an adjacent location with non-zero probability
- for each location with non-zero probability, we do the following:
- check if each of 4 movements (north/south/east/west) is possible — that is, does not result in the robot going off the board or into a wall
- if so, we temporarily set the probability of that movement to 0.25
- we then set the probability of staying put to 1 minus the sum of the probabilities of the above movements
- going back to the blank probability state, we add to each state the following:
- the probability of being at each previous state the given state is reachable from, times the probability of having made the move from that previous state
- (this is kind of a long and clunky series of calculations since I don't understand linear algebra and don't know what a matrix is, but it works!)

**update()**

- a lot simpler than the previous function — we simply grab a color from the sensor readings and then loop through possible locations
- if the color of that location matches the sensor reading, we multiply probability by 0.88; if not, by 0.04
- the normalize() function calcluates a factor to multiply every probability by to make sure it still adds up to 1

**filter()**

- we put everything together — for every sensor reading we call predict() and update()

I also wrote solve() which runs filter() and displays the actual path alongside the predicted path (that is, most likely location during each time step).
# Testing
I built a RandomWalk class to just generate a random path, valid path for comparison. Results for number of mistakes on all 3 mazes below:
<pre>
| trials | maze 1  | maze 2  | maze 3  |
| ------ | ------- | ------- | ------- |
| 1      | 16      | 14      | 15      |
| 2      | 14      | 15      | 16      |
| 3      | 13      | 14      | 16      |
| 4      | 16      | 15      | 15      |
| 5      | 10      | 10      | 14      |
| 6      | 15      | 16      | 11      |
| 7      | 14      | 16      | 13      |
| 8      | 15      | 13      | 10      |
| 9      | 11      | 16      | 9       |
| 10     | 16      | 16      | 16      |
| ------ | ------- | ------- | ------- |
| avg    | 14      | 14.5    | 13.5    |
| %      | 0.125   | 0.09375 | 0.15625 |
</pre>
These are chance probabilities. Reference for comparison below.\
\
As for HMM.py, I ran solve() several times. Example result below:
<pre>
at each time step:
location		prediction
---				---
[1, 1]			[[1, 1]]
[0, 1]			[[1, 0]]
[0, 1]			[[1, 0]]
[1, 1]			[[1, 1]]
[1, 1]			[[1, 1]]
[1, 0]			[[1, 0]]
[1, 0]			[[1, 0]]
[1, 0]			[[1, 0]]
[1, 0]			[[1, 1]]
[1, 0]			[[1, 1]]
[1, 0]			[[1, 0]]
[1, 0]			[[1, 0]]
[1, 0]			[[1, 0]]
[1, 0]			[[1, 0]]
[1, 0]			[[1, 0]]
[1, 1]			[[1, 1]]
</pre>
Here is a table displaying accuracy over 10 trials on maze3.maz, each one consisting of 16 random moves and scans run on maze 1. I consider the prediction at each timestep to be correct if the actual path matches the predicted path, or if it matches one of several members of a predicted path list (given that sometimes multiple locations have the same probability):
<pre>
| trials | actual end | predicted end | percent accuracy |
| ------ | ---------- | ------------- | ---------------- |
| 1      | [1, 1]     | [1, 1]        | 0.75             |
| 2      | [0, 2]     | [0, 2]        | 0.75             |
| 3      | [1, 0]     | [1, 0]        | 0.875            |
| 4      | [0, 1]     | [0, 3]        | 0.5625           |
| 5      | [1, 1]     | [1, 1]        | 0.75             |
| 6      | [1, 3]     | [0, 2]        | 0.625            |
| 7      | [0, 2]     | [0, 2]        | 0.75             |
| 8      | [1, 0]     | [1, 0]        | 0.9375           |
| 9      | [0, 2]     | [0, 2]        | 0.8125           |
| 10     | [1, 0]     | [1, 0]        | 0.9375           |
| ------ | ---------- | ------------- | ---------------- |
| avg    | n/a        | n/a           | 0.775            |
</pre>
As we can see, my algorithm returns a path reasonably similar to the actual path. 80% of trials returned the correct endpoint, and 77.5% of predictions are correct. This is significantly better than chance. Also, actual start and predicted start always have the same color, even if they don't match.\
\
I'd also like to note that when I ran the algorithm on maze2.maz (which has no walls), the algorithm still usually returns the correct endpoint, but there are more mistakes in the path. Two factors contribute to this — fewer walls means more possible paths and therefore the prediction is more often wrong, and more floors means more opportunities for the color sensor to make mistakes.\
\
Results for other mazes here:
<pre>
maze 1
| trials | mistakes | percent accuracy |
| ------ | -------- | ---------------- |
| 1      | 9        | 0.4375           |
| 2      | 7        | 0.5625           |
| 3      | 3        | 0.8125           |
| 4      | 6        | 0.625            |
| 5      | 9        | 0.4375           |
| 6      | 0        | 1                |
| 7      | 3        | 0.8125           |
| 8      | 13       | 0.1825           |
| 9      | 7        | 0.5625           |
| 10     | 3        | 0.8125           |
| ------ | -------- | ---------------- |
| avg    | 6        | 0.625            |

maze 2
| trials | mistakes | percent accuracy |
| ------ | -------- | ---------------- |
| 1      | 7        | 0.5625           |
| 2      | 6        | 0.625            |
| 3      | 6        | 0.625            |
| 4      | 11       | 0.3125           |
| 5      | 11       | 0.3125           |
| 6      | 5        | 0.6875           |
| 7      | 6        | 0.625            |
| 8      | 3        | 0.8125           |
| 9      | 4        | 0.75             |
| 10     | 6        | 0.625            |
| ------ | -------- | ---------------- |
| avg    | 6.5      | 0.59375          |
</pre>
As we can see, they're not that accurate but still higher than 0.5 and still much higher than random walk results.
# Extensions
## BONUS_RandomWalk.py
Not sure if this counts as an extension, but I implemented a brief algorithm to just take a brief, legal random walk. The bulk of this lies in my data analysis — the generated random walk allows me to compare my HMM/Viterbi results with results generated by chance, which is helpful in demonstrating that they work.
## BONUS_Viterbi.py
I implemented a generalized Viterbi algorithm in the Viterbi class and applied it to solving our specific problem in ViterbiSolver. Description below:

**Viterbi**

- takes in observations, states, initial probabilities, transition probabilities, emission probabilities
- multiplies probabilities at each time step for each condition using the information given above
- selects best final state, then backtracks to construct entire path

**Application**
- ViterbiSolver builds observations, states, initial probabilities, transition probabilities, and emission probabilities from the provided robot model
- observations = sensor readings
- states = possible locations 0-15
- transition probabilities = 2D array of probabilities of going between each state pair
- emission probabilities = probability of reading each color at each location
- run viterbi with these

When I tested my Viterbi code on all three mazes, it tends less accurate than HMM.py but still more accurate than a random walk. Table below:
<pre>
maze 1
| trials | mistakes | percent accuracy |
| ------ | -------- | ---------------- |
| 1      | 14       | 0.125            |
| 2      | 10       | 0.625            |
| 3      | 16       | 0                |
| 4      | 8        | 0.5              |
| 5      | 10       | 0.375            |
| 6      | 13       | 0.1875           |
| 7      | 3        | 0.8125           |
| 8      | 7        | 0.5625           |
| 9      | 9        | 0.4375           |
| 10     | 6        | 0.625            |
| ------ | -------- | ---------------- |
| avg    | 9.6      | 0.4              |

maze 2
| trials | mistakes | percent accuracy |
| ------ | -------- | ---------------- |
| 1      | 14       | 0.125            |
| 2      | 10       | 0.375            |
| 3      | 16       | 0                |
| 4      | 14       | 0.125            |
| 5      | 2        | 0.875            |
| 6      | 10       | 0.375            |
| 7      | 11       | 0.3125           |
| 8      | 15       | 0.0625           |
| 9      | 12       | 0.25             |
| 10     | 16       | 0                |
| ------ | -------- | ---------------- |
| avg    | 12       | 0.25             |

maze 3
| trials | mistakes | percent accuracy |
| ------ | -------- | ---------------- |
| 1      | 2        | 0.875            |
| 2      | 3        | 0.8125           |
| 3      | 9        | 0.4375           |
| 4      | 7        | 0.5625           |
| 5      | 8        | 0.5              |
| 6      | 6        | 0.625            |
| 7      | 11       | 0.3125           |
| 8      | 4        | 0.75             |
| 9      | 7        | 0.5625           |
| 10     | 9        | 0.4375           |
| ------ | -------- | ---------------- |
| avg    | 6.6      | 0.5875           |
</pre>
My Viterbi implementation doesn't work that well on maze2.maz but it's still almost 3 times more accurate than by chance.
## BONUS_forward_backward.py
Like Viterbi, the forward-backward algorithm also takes in observations, states, initial probabilities, transition probabilities, and emission probabilities. Calculated the same way as in Viterbi. This is how I implemented the actual algorithm:\
\
This algorithm basically calculates alpha and beta in the form of 2D arrays. Alpha/forward represents the probability of being in a particular state at each time given the observations up to that point, and beta/backward calculates the probability of observing the rest of the sequence from a particular state at a particular time step. The function forward_backward() combines both of them to return the most likely path with the highest probability.
<pre>
maze 1
| trials | mistakes | percent accuracy |
| ------ | -------- | ---------------- |
| 1      | 5        | 0.6875           |
| 2      | 4        | 0.75             |
| 3      | 1        | 0.9375           |
| 4      | 5        | 0.6875           |
| 5      | 7        | 0.5625           |
| 6      | 1        | 0.9375           |
| 7      | 6        | 0.625            |
| 8      | 10       | 0.375            |
| 9      | 3        | 0.8125           |
| 10     | 4        | 0.75             |
| ------ | -------- | ---------------- |
| avg    | 4.6      | 0.7125           |

maze 2
| trials | mistakes | percent accuracy |
| ------ | -------- | ---------------- |
| 1      | 3        | 0.8125           |
| 2      | 7        | 0.5625           |
| 3      | 2        | 0.875            |
| 4      | 8        | 0.5              |
| 5      | 12       | 0.25             |
| 6      | 7        | 0.5625           |
| 7      | 5        | 0.6875           |
| 8      | 7        | 0.5625           |
| 9      | 5        | 0.6875           |
| 10     | 2        | 0.875            |
| ------ | -------- | ---------------- |
| avg    | 5.8      | 0.6375           |

maze 3
| trials | mistakes | percent accuracy |
| ------ | -------- | ---------------- |
| 1      | 5        | 0.6875           |
| 2      | 3        | 0.8125           |
| 3      | 5        | 0.6875           |
| 4      | 3        | 0.8125           |
| 5      | 9        | 0.4375           |
| 6      | 4        | 0.75             |
| 7      | 6        | 0.625            |
| 8      | 3        | 0.8125           |
| 9      | 2        | 0.875            |
| 10     | 2        | 0.875            |
| ------ | -------- | ---------------- |
| avg    | 4.2      | 0.7375           |
</pre>
This algorithm outperforms both HMM and Viterbi on maze1.maz and maze2.maz. It performs slightly worse than HMM on maze3.maz. Overall, this is the most accurate one so far.
## BONUS_VisualizePath.py
I spent about 10 hours on this.Downloaded PyQt6 because PyQt5 seems incompatible with my laptop's compiler, somehow? (There is probably a fix I haven't figured out.)\
\
Basically this is a GUI to display the path the robot takes in the form of a circle, as well as the three predictions with the highest probability scores (shaded varying depths of blue). I implemented a counter to cycle through different steps, and a lot of converting between coordinates and indices.\
\
To spare you the agony of having to download and configure PyQt6 (which has different functions from PyQt5!) I have included a video of my visualization in action.
# Bonus: Literature Review
## Extrapolation Methods for Accelerating PageRank Computations (Kamvar et al.)
PageRank is an algorithm created to determine the relevance of web pages by computing the principal eigenvector of the web graph matrix. The authors of the paper proposed a new method, quadratic extrapolation, for computing PageRank faster. Quadratic Extrapolation assumes that the principal eigenvector can be expressed as a linear combination of the first three eigenvectors in the matrix, and this leads to a simpler representation and therefore faster calculation. By continuously subtracting non-principle eigenvectors through successive iterations, quadratic extrapolation is able to significantly decrease runtime by speeding up convergence of the power method (standard method for calculating eigenvectors).