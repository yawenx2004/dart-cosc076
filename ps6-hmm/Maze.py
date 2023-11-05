# author: @yawen_xue
# date: 26 oct. 23
# purpose: maze class for hmm; somewhat based on ps2 maze

class Maze:
    def __init__(self, filename):
        self.layout, self.robotloc = self.load_maze(filename)
        self.width = len(self.layout[0])
        self.height = len(self.layout)

    def load_maze(self, filename):
        """
        helper function to load file
        :param filename:
        :return:
        """
        layout = []
        robotloc = []

        file = open(filename, "r")
        for line in file:
            # get robot location
            if line[0] == "\\":
                words = line.split()
                robotloc.append(int(words[1]))
                robotloc.append(int(words[2]))

            # loop through each row to get maze layout
            else:
                row = []
                for i in range(0, len(line.strip())):
                    row.append(line[i])
                layout.append(row)
        file.close()

        return layout, robotloc

    def get_color(self, x, y):
        """
        returns color of coordinate
        :param x:
        :param y:
        :return:
        """
        i = self.width - 1 - y
        return self.layout[i][x]

    def get_color_index(self, index):
        """
        same function as above, adapted to list representations of map locations
        :param index:
        :return:
        """
        x = int(index % self.width)
        y = int(index / self.width)
        return self.get_color(x, y)

    def is_floor(self, x, y):
        """
        returns true if given coordinate is floor (that is, #)
        :param x:
        :param y:
        :return:
        """
        # not floor if outside maze
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False

        # not floor if is wall
        if self.get_color(x, y) == "#":
            return False

        return True

    def is_floor_index(self, index):
        """
        same function as above, adapted to list representations of map locations
        :param index:
        :return:
        """
        x = int(index % self.width)
        y = int(index / self.width)
        return self.is_floor(x, y)

    def has_robot(self, x, y):
        """
        returns true if given coordinate contains robot
        :param x:
        :param y:
        :return:
        """
        if self.robotloc == [x, y]:
            return True

        return False
