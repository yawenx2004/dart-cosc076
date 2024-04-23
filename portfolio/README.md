# Contents
1. [TL;DR](#-tldr-)
2. [Introduction](#introduction-)
    - [Key Concepts](#key-concepts)
3. [PRM & the Arm Robot](#prm--the-arm-robot-)
4. [RRT](#rrt-)
5. [Code Design & Implementation](#code-design--implementation-%EF%B8%8F)
    - [PRM Implementation](#prm-implementation)
    - [RRT Implementation](#rrt-implementation)
6. [Testing](#testing-)
    - [PRM Demo](#prm-demo)
    - [RRT Testing](#rrt-testing)
7. [Conclusion](#conclusion-)

# 💡 TL;DR 💡
This report is running so much longer than I expected it to so here are a few salient points:

- PRM & RRT algorithms for robotic motion planning

- While implementing RRT I encountered the common problem of the search tree getting stuck in various places due to obstacles and narrow passages. To address this, I implementing an **unstuck()** function which briefly samples points in different directions to continue exploration. 🌟

    - See [RRT Testing](#rrt-testing) for details; this is probably the most interesting part of the report.

- Testing has indicated that the above fix works!

- COSC 76 is very fun. If you're at Dartmouth, take it!

# Introduction 🌱 
In fall of 2023 I took COSC 76/COGS 44: Artificial Intelligence at Dartmouth College, where I read about and implemented various algorithms designed to solve computational problems vaguely related to artificial intelligence. This here is a cleaned-up version of our final project: **PRM & RRT for robotic motion planning** 🔧🤖.

It is currently spring of 2024, and since then I've taken an actual algorithms class. Though I find myself wishing I'd waited until after I've learned algorithms to take Artificial Intelligence (in hindsight there's a lot more I could've learned if only I had an understanding of more basic things to scaffold upon), this nevertheless remains a part of my academic journey that has inspired me very much, and I'm quite proud of it. I would love to do something algorithms-related in the future.

My original code and report can be found [here](https://github.com/yawenx2004/dart-cosc076/tree/main/ps7-prm-rrt).

### Key Concepts
**Robotic motion planning** is an artificial intelligence problem where we generate a sequence of valid configurations that allows a robot to move from an initial state to a goal state in an environment, while avoiding collisions. Two examples of robotic motion planning algorithms are PRM and RRT, both of which involve randomly sampling a configuration space.

- **Probabilistic roadmap (PRM):** connects randomly-sampled valid configurations in the environment and connects them to form a network, then searches through the network to find a path.

- **Rapidly-exploring Random Tree (RRT):** builds a tree by randomly sampling points in the configuration space; each new randomly-sampled node is connected to the nearest node on the tree.

Both of these algorithms involve **discretizing a continuous search space**, a topic I first encountered in this class and have been fascinated by ever since.

Now that we've defined the algorithms, let's move on to the specific implementations in this project.

# PRM & the Arm Robot 🔧🤖

- **Input:**

    - **robot**, in this case a 2D planar arm consisting of n lines

    - **obstacles**, represented as 2D polygons

    - **start configuration**, represented as an n-array, each element indicating the angle of a section of the robotic arm

    - **goal configuration**, similar to start configuration

- **Output**: sequence of valid arm configurations that allow the arm to move from start to goal, without bumping into obstacles

# RRT 🛼🚀

- **Input:**

    - **environment**, here a 2D plane filled with obstacles represented as 2D polygons

    - **start point**, somewhere within the environment

    - **goal point**, somewhere else within the environment

- **Output:** a path from the start to the end that avoids collision with obstacles

# Code Design & Implementation 🛠️
As of 22 April 2024 I have rewritten the code from last fall; you can find them [here](/PRM) (PRM) and [here](/RRT) (RRT). Original code is [here](https://github.com/yawenx2004/dart-cosc076/tree/main/ps7-prm-rrt).

**Note:** We are using the intersects() function of the shapely library to check for collisions, and using matplotlib to visualize. Search/solve is done through a simple BFS.

### PRM Implementation
Our PRM has three parts—ArmRobot.py to represent the arm robot, PRM.py which houses the actual PRM implementation, and PRMSolver.py which uses BFS to search the PRM graph and find a solution.

#### ArmRobot.py:

- **__init__** takes parameters num_joints (number of joints/links the robotic arm has) and start_config (starting angle for each joint); initially sets self.config to start_config

- **forward_kinematics()** calculates the Cartesian location of each joint given the angle specified in its configuration

- **collids_with()** uses the intersects() function of the shapely library to check for collision between a given configuration and a given set of obstacles

#### PRM.py:

- **__init__** takes an ArmRobot instance, a goal configuration, and a list of obstacles as its parameters, as well as values k (max edges each vertex can have in the roadmap) and num_samples (number of vertices the roadmap will have)

- **sample()** randomly selects valid configurations (that is, configurations that do not result in the arm passing through obstacles); these form the vertices of the roadmap

- **add_edges()** loops through the configurations sampled, and for each vertex v it looks at k nearest neighbors and adds an edge from v to its neighbor if you can go from v to that neighbor without colliding into an obstacle

    - **get_neighbors()** returns k nearest neighbors using a KD tree

    - **is_collision()** checks for collisions using linear interpolation

- **get_roadmap()** runs sample(), runs add_edges(), thus generating and returning the PRM roadmap (alongside the start and goal configurations)

- **visualize()** animates the path—if we find one—by plotting frame-by-frame each step in the path

#### PRMSolver.py:
PRMSolver.py runs get_roadmap() to get the roadmap, then runs BFS on edges to find the shortest path from the start to the goal within the roadmap. Animates the path, too, with the visualize() function described above, if that optional parameter to do so is toggled on.

PRM *done*! 🎉

Onto RRT.

### RRT Implementation
🚧

# Testing 🐞🔍
### PRM Demo
In test_prm.py I have written several test cases for an 2R planar robot and a 4R planar robot (this one with environments of varying difficulty). To select the test case, just comment out lines as specified in the Python file. When you run test_prm.py in its current form you should see, aside from the solution in the console, a matplotlib animation of an arm moving from the start to the goal configuration.

First, let's take a look at the 2R test case. Here, configurations are 2-vectors and can therefore be mapped onto 2D space. Below is the graph that represents the PRM roadmap. Vertices represent possible configurations (red = start; yellow = goal), and edges represent the possibility of going between two configurations without collision.

![Figure 1.](figures/prm-2r-samples.png)

This is the map PRMSolver uses BFS to search through. The shortest path from the red vertex to the yellow vertex represents the solution.
```
Solution found after searching 4414 nodes!
---
PATH: [(85, 0), (110.29536799915928, 161.16394618103706), (200, 350)]
LENGTH: 3
```

Here's the same problem, visualized another way. Here, red polygons represent obstacles, the red configuration represents the start configuration, the yellow configuration represents the goal configuration, and the blue ones represent every configuration sampled. This is another way to look at the roadmap.

![Figure 2.](figures/prm-2r-configs.png)

Now let's take a look at higher-dimensional problems. For the hardest 4R problem (environment and generated configurations pictured below), PRM returned the following output—

```
Solution found after searching 938 nodes!
---
PATH: [(0, 0, 0, 300), (132.56911930250288, 218.5923196635714, 219.15960059395246, 237.24818972150314), (210, 330, 90, 75)]
LENGTH: 3
```
A visualization of the problem—
![Figure 3.](figures/prm-4r-hardest-configs.png)

**Note:** This test case runs in about 15 seconds if you choose to visualize, but due to matplotlib loading time, if you do choose to visualize, it will take quite a bit longer.

### RRT Testing
🚧

# Conclusion 🌿
🚧
