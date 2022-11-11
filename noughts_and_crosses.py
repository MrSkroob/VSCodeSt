from __future__ import annotations
import random


class Marker(): # piece that each player will place
    def __init__(self, character: str) -> None:
        self._character = character

    def __str__(self) -> str:
        return self._character
    
    def __eq__(self, other: Marker):
        return str(self) == str(other)


class Board():
    def __init__(self, collumns: int, rows: int) -> None:
        # i would've added an option for non square boards, but it breaks :(
        self._COLLUMN_SIZE = collumns
        self._ROW_SIZE = rows
        self._SQUARES = collumns * rows
        self._data = [Marker('_')] * self._SQUARES
    
    def get_collumns(self):
        return self._COLLUMN_SIZE
    
    def get_rows(self):
        return self._ROW_SIZE
    
    def get_squares(self):
        return self._SQUARES
    
    def get_marker_at_position(self, collumn: int, row: int):
        """Returns a marker and its index within the board list"""
        if collumn < 0 or row < 0:
            raise IndexError("Escaped board")
        if collumn > self._COLLUMN_SIZE or row > self._ROW_SIZE:
            raise IndexError("Escaped board")
        index = ((row * self._COLLUMN_SIZE)) + collumn
        marker: Marker = self._data[index]
        return marker, index

    def get_collumn_row_at_index(self, index: int):
        """Returns the collumn and row from an index"""
        collumn = index % self._COLLUMN_SIZE
        row = index // self._COLLUMN_SIZE # // self._ROW_SIZE
        return collumn, row
        
    def set_cell(self, collumn: int, row: int, marker: Marker) -> bool:
        """Adds a marker to a position on the board. Returns a boolean depending on success"""
        collumn -= 1
        row -= 1
        try:
            currently_occupied, index = self.get_marker_at_position(collumn, row)
        except IndexError:
            return False
        if str(currently_occupied) == '_':
            self._data[index] = marker
            return True
        else:
            return False
    
    def check_win(self):
        """Returns a marker object of who (or what) won."""
        offsets = ( # offsets by collumn, row
            (-1, -1), # top_left
            (0, -1), # top
            (1, -1), # top_right
            (-1, 0), # left
            (1, 0), # right
            (-1, 1), # bottom_left
            (0, 1), # bottom
            (1, 1), # bottom_right
        )
        rows_to_win = 5
        checked = [False] * self._SQUARES
        for i, marker in enumerate(self._data):
            marker_str = str(marker)
            if marker_str != "_": # only check if space isn't empty
                if not checked[i]: # pieces that have checked around them
                    for offset in offsets: # check around the current piece
                        collumn, row = self.get_collumn_row_at_index(i) # convert current position into the collumn and row
                        successes = 1
                        try:
                            while True:
                                adj_marker, index = self.get_marker_at_position(collumn + offset[0], row + offset[1]) # get adjacvent marker
                                if checked[index]:
                                    break
                                if adj_marker == marker:
                                    collumn, row = self.get_collumn_row_at_index(index) # if matched, continuing offsetting the same way
                                    successes += 1
                                else:
                                    break # try the next offset if adjacent marker doesn't match.
                        except IndexError: # if the offset exits out of the board, catch the index error and try the next offset.
                            pass
                        if successes == rows_to_win:
                            return marker
                    checked[i] = True
        return None
    
    def __str__(self):
        string = ".___" * self._COLLUMN_SIZE + ".\n"
        for i, marker in enumerate(self._data):
            collumn, _ = self.get_collumn_row_at_index(i)
            if collumn == self._COLLUMN_SIZE - 1:
                string += "| " + str(marker) + " |"
                string += "\n" + "|___" * self._COLLUMN_SIZE + "|\n"
            else:
                string += "| " + str(marker) + " "
        return string

game_board = Board(5, 5)
player = Marker("X")
enemy = Marker("O")

for i in range(5 * 5):
    collumn, row = game_board.get_collumn_row_at_index(i)
    if random.randint(0, 1) == 1:
        piece = Marker("O")
    else:
        piece = Marker("X")
    game_board.set_cell(collumn + 1, row + 1, piece)

print(game_board)
print(game_board.check_win())
