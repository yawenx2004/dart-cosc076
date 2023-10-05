from Maze import Maze
from collections import deque

class Wavefront:
    def __init__(self, maze, goal):
        self.maze = maze
        self.goal = goal
        self.start = maze.robotloc

    def get_successors(self, state):
        x, y = state
        successors = []

        # north, south, east, west
        moves = [(0, 1), (0, -1), (-1, 0), (1, 0)]

        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy

            if self.maze.is_floor(new_x, new_y):
                successors.append((new_x, new_y))

        return successors

    def wavefront_bfs(self):
        queue = deque()
        wavefront = {}

        queue.append(self.goal)
        wavefront[self.goal] = 0

        while queue:
            curr = queue.pop()

            for neighbor in self.get_successors(curr):
                if neighbor not in wavefront:
                    wavefront[neighbor] = wavefront[curr] + 1
                    queue.append(neighbor)

        return wavefront


if __name__ == "__main__":
    test_maze = Maze("maze11.maz")
    test_mp = Wavefront(test_maze, (2, 5))
    print(test_mp.wavefront_bfs())