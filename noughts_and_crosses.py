class Marker():
    def __init__(self, character: str) -> None:
        self._character = character
        pass

    def __str__(self) -> str:
        return self._character


class Board():
    def __init__(self) -> None:
        self.ROW_SIZE = 3
        self.COLLUMN_SIZE = 3
        self.TOTAL_SIZE = self.ROW_SIZE * self.COLLUMN_SIZE
        self.data = [Marker('_')] * (self.ROW_SIZE * self.COLLUMN_SIZE)
    
    def __str__(self):
        display = []
        string = ""
        for i in range(self.ROW_SIZE):
            display.append([])
            for j in range(self.COLLUMN_SIZE):
                index = ((i * 3)) + j
                marker = self.data[index]
                display[i].append(marker)
                string += str(marker)
            string += "\n"
        return string
        

    def set_cell(self, x: int, y: int, marker: Marker) -> bool:
        """Adds a marker to a position on the board. Returns a boolean depending on success"""
        currently_occupied = self.data[((x * 3) - 1) + y]
        if currently_occupied == ' ':
            self.data[((x * 3) - 1) + y] = marker
            return True
        else:
            return False


game_board = Board()
print(game_board)