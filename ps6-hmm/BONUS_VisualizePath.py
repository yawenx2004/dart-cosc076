import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor, QPainter, QPen
from Maze import Maze


class VisualizePath(QWidget):
    def __init__(self, maze, states_history, actual_path):
        super().__init__()

        # given info
        self.maze = maze
        self.states_history = states_history
        self.actual_path = actual_path

        # canvas
        self.setWindowTitle("path animation")
        self.setGeometry(100, 100, 200, 200)

        # to change
        self.colors = self.set_initial_colors()
        self.color_sequence = self.get_color_sequence()

        # steps
        self.counter = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_colors)
        self.timer.start(1000)  # every second
        self.show()

    def get_color_sequence(self):
        """
        uses states_history to build sequence of colors —
        that is, sequence of most probable movements
        :return:
        """
        s = []

        # for each location
        for i in range(0, len(self.states_history)):

            # get three most likely locations
            max1 = []
            max2 = []
            max3 = []

            # loop through all probabilities for each location and turn into dictionary
            dict = {}
            for j in range(0, len(self.states_history[i])):
                key = self.states_history[i][j]
                if key != 0:
                    if key in dict:
                        entry = dict[key]
                        entry.append(j)
                    else:
                        entry = [j]
                    dict[key] = entry

            # use dictionary to find most likely locations
            max_prob1 = max(list(dict.keys()))
            max1 = dict[max_prob1]
            dict.pop(max_prob1)
            if dict:
                max_prob2 = max(list(dict.keys()))
                max2 = dict[max_prob2]
                dict.pop(max_prob2)
            if dict:
                max_prob3 = max(list(dict.keys()))
                max3 = dict[max_prob3]

            s.append([max1, max2, max3])
        return s

    def update_colors(self):
        """
        updates at each time step, using counter to determine next course of action
        :return:
        """
        self.colors = self.set_initial_colors()
        s = self.color_sequence[self.counter % 16]

        # color three most likely locations various shades of green
        for i in s[0]:
            x = i % 4
            y = i // 4
            self.colors[x][3 - y] = QColor(80, 66, 207)
        for i in s[1]:
            x = i % 4
            y = i // 4
            self.colors[x][3 - y] = QColor(101, 127, 219)
        for i in s[2]:
            x = i % 4
            y = i // 4
            self.colors[x][3 - y] = QColor(151, 200, 240)

        # update counter
        self.counter += 1
        self.update()

    def set_initial_colors(self):
        """
        sets initial colors as 2d array representing rows and columns of the maze
        :return:
        """
        colors = []
        for i in range(0, 4):
            c = []
            for j in range(0, 4):
                x = i
                y = 3 - j

                # black if wall, white if floor
                if self.maze.is_floor(x, y):
                    c.append(QColor(255, 255, 255))
                else:
                    c.append(QColor(0, 0, 0))

            colors.append(c)
        return colors

    def paintEvent(self, event):
        """
        draw!
        :param event:
        :return:
        """
        painter = QPainter(self)
        pen = QPen()
        square_size = min(self.width(), self.height()) // 4

        # loop through maze
        for i in range(0, 4):
            for j in range(0, 4):
                w = i * square_size
                h = j * square_size

                # fill colors accordingly
                painter.fillRect(w, h, square_size, square_size, self.colors[i][j])

                # draw walls
                x = i
                y = 3 - j
                if not self.maze.is_floor(x, y):
                    painter.fillRect(w + int(square_size / 4),
                                     h + int(square_size / 4),
                                     int(square_size / 2),
                                     int(square_size / 2),
                                     QColor(0, 0, 0))

            # draw circle in current location
            curr_loc = self.actual_path[(self.counter - 1) % 16]
            x = curr_loc[0]
            y = 3 - curr_loc[1]

            pen.setWidth(3)
            pen.setColor(QColor(0, 0, 0))
            painter.setPen(pen)
            painter.drawEllipse(int(x * square_size + square_size / 4),
                                int(y * square_size + square_size / 4),
                                int(square_size / 2),
                                int(square_size / 2))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    maze = Maze("mazes/maze1.maz")
    window = VisualizePath(maze, 1, 1)
    sys.exit(app.exec())
