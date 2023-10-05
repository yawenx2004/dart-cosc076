# author: @yawen_xue
# date: 5 oct. 23
# purpose: opening book for chess ai

import chess

class OpeningBook():
    def __init__(self):
        self.openings = {
            "": [],
            "italian_game": ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"],
            "kings_gambit": ["e2e4", "e7e5", "f2f4"]
        }

    def get_opening(self, opening_name):
        """
        returns move given by name plus side
        :param opening_name:
        :return:
        """
        return self.openings[opening_name]

# bit of test code
if __name__ == "__main__":
    op = OpeningBook()
    print(op.get_opening("italian_game"))