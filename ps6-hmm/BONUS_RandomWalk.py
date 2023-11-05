# author: @yawen_xue
# date: 4 nov. 23
# purpose: for more refined testing

from random import choice
from Maze import Maze


class RandomWalk:
    def __init__(self, maze, num_steps=16):
        self.maze = maze
        self.path = []
        self.walk(num_steps)

    def walk(self, num_steps):
        """
        take steps
        :param num_steps:
        :return:
        """
        for i in range(0, num_steps):
            self.step()

    def step(self):
        """
        single random step
        :return:
        """
        # choose random move
        moves = [[0, 1], [0, -1], [1, 0], [-1, 0]]  # n, s, e, w
        move = choice(moves)

        # move robot if legal
        newloc = [self.maze.robotloc[0] + move[0], self.maze.robotloc[1] + move[1]]
        if self.maze.is_floor(newloc[0], newloc[1]):
            self.maze.robotloc = newloc

        self.path.append(self.maze.robotloc)


# bit of test code
if __name__ == "__main__":
    maze1 = Maze("mazes/maze1.maz")
    walk = RandomWalk(maze1)
    print(walk.path)
