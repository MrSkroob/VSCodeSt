from __future__ import annotations
import time
import random


class Marker(): # piece that each player will place
    def __init__(self, character: str) -> None:
        self._character = character

    def __str__(self) -> str:
        return self._character
    
    def __eq__(self, other: Marker):
        return str(self) == str(other)


class Board():
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
    
    def __init__(self, collumns: int, rows: int, rows_to_win: int) -> None:
        self._COLLUMN_SIZE = collumns
        self._ROW_SIZE = rows
        self._SQUARES = collumns * rows
        self._ROWS_TO_WIN = rows_to_win
        self._data = [Marker('_')] * self._SQUARES
    
    def get_collumns(self):
        return self._COLLUMN_SIZE
    
    def get_rows(self):
        return self._ROW_SIZE
    
    def get_squares(self):
        return self._SQUARES
    
    def get_rows_to_win(self):
        return self._ROWS_TO_WIN
    
    def get_data(self):
        return self._data
    
    def get_marker_at_position(self, collumn: int, row: int):
        """Returns a marker and its index within the board list"""
        if collumn < 0 or row < 0:
            raise IndexError("Escaped board")
        if collumn > self._COLLUMN_SIZE - 1 or row > self._ROW_SIZE - 1:
            raise IndexError("Escaped board")
        index = ((row * self._COLLUMN_SIZE)) + collumn
        marker: Marker = self._data[index]
        return marker, index

    def get_collumn_row_at_index(self, index: int):
        """Returns the collumn and row from an index"""
        collumn = index % self._COLLUMN_SIZE
        row = index // self._COLLUMN_SIZE # // self._ROW_SIZE
        return collumn, row

    def _set_cell_directly(self, index, marker):
        """Directly adds a marker to the board - no checking"""
        self._data[index] = marker

    def set_cell(self, collumn: int, row: int, marker: Marker) -> bool:
        """Adds a marker to a position on the board. Returns a boolean depending on success, raises index error if board full"""
        empty = 0
        for i in self._data:
            if str(i) != "_":
                empty += 1
        if empty == self._SQUARES:
            raise IndexError("Board full!")
        try:
            currently_occupied, index = self.get_marker_at_position(collumn, row)
        except IndexError:
            return False
        if str(currently_occupied) == '_':
            self._data[index] = marker
            return True
        else:
            return False
    
    def check_win(self) -> Marker:
        """Returns a marker object of who (or what) won."""
        for i, marker in enumerate(self._data):
            marker_str = str(marker)
            if marker_str != "_": # only check if space isn't empty
                for offset in self.offsets: # check around the current piece
                    collumn, row = self.get_collumn_row_at_index(i) # convert current position into the collumn and row
                    successes = 1
                    try:
                        while True:
                            adj_marker, index = self.get_marker_at_position(collumn + offset[0], row + offset[1]) # get adjacvent marker
                            if adj_marker == marker:
                                collumn, row = self.get_collumn_row_at_index(index) # if matched, continuing offsetting the same way
                                successes += 1
                            else:
                                break # try the next offset if adjacent marker doesn't match.
                    except IndexError: # if the offset exits out of the board, catch the index error and try the next offset.
                        pass
                    if successes == self._ROWS_TO_WIN:
                        return marker
        return Marker("_")
    
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


class Player():
    def __init__(self, marker: str, board: Board) -> None:
        self._marker = Marker(marker)
        self._board = board
    
    def get_marker(self):
        return self._marker

    def get_move(self):
        """Gets a valid move from the user"""
        board = self._board
        max_collumns = board.get_collumns()
        max_rows = board.get_rows()
        collumn, row = 0, 0
        while not (collumn in range(1, max_collumns - 1) and row in range(1, max_rows - 1)):
            try:
                collumn = int(input(f"Which collumn? (1 - {max_collumns})"))
                row = int(input(f"Which row? (1 - {max_rows})"))
            except ValueError:
                pass
            else:
                break
        return collumn - 1, row - 1
    
    def apply_move(self):
        """More or less 'gui' interface for inputing a move."""
        collumn, row = self.get_move()
        self._board.set_cell(collumn, row, self._marker)
        # self._board.set_cell_directly(index, self._marker)


class Bot(Player):
    def __init__(self, marker: str, board: Board) -> None:
        super().__init__(marker, board)
    
    def get_threats(self, minimum_threat: int, attack: bool):
        """Returns a list of threat locations. Each location includes the ((collumn0, row0), (offsetcollumn0, offsetrow0), successes), ((collumn1, row1), (offsetcollumn1, offsetrow1)
        Also accepts boolean to attack instead of defend"""
        board = self._board
        threats = []
        checked = [False] * board._SQUARES
        for i, marker in enumerate(board.get_data()):
            marker_str = str(marker)
            if marker_str != "_" and (marker != self._marker and not attack) or (marker == self._marker and attack): # only check if space isn't empty
                if not checked[i]:
                    for offset_i, offset in enumerate(board.offsets): # check around the current piece
                        mark_as_checked = []
                        collumn, row = board.get_collumn_row_at_index(i) # convert current position into the collumn and row
                        start_collumn, start_row = collumn, row
                        successes = 1
                        spaces = 0
                        try:
                            while True:
                                adj_marker, index = board.get_marker_at_position(collumn + offset[0], row + offset[1]) # get adjacvent marker
                                if adj_marker == marker or (str(adj_marker) == "_" and spaces == 0):
                                    collumn, row = board.get_collumn_row_at_index(index) # if matched, continuing offsetting the same way
                                    mark_as_checked.append(index)
                                    if str(adj_marker) == "_":
                                        try:
                                            adj_marker_, _ = board.get_marker_at_position(collumn + offset[0], row + offset[1])
                                            spaces += 1
                                        except IndexError:
                                            pass
                                        else:
                                            if adj_marker_ == marker:
                                                print("Space found", collumn, row)
                                                threats.append((((start_collumn, start_row), board.offsets[len(board.offsets) - offset_i - 1], successes + 1), ((collumn, row), (0, 0))))
                                    else:
                                        successes += 1
                                else:
                                    break # try the next offset if adjacent marker doesn't match.
                        except IndexError: # if the offset exits out of the board, catch the index error and try the next offset.
                            pass
                        else:
                            if successes >= minimum_threat:
                                for marked in mark_as_checked:
                                    checked[marked] = True 
                                threats.append((((start_collumn, start_row), board.offsets[len(board.offsets) - offset_i - 1], successes), ((collumn, row), (0, 0))))
                                break
        return threats

    def get_random_move(self):
        """Returns a random move. Returns 0, 0, by default if no moves found."""
        board = self._board
        collumn, row = 0, 0
        valid_moves = []
        for i, v in enumerate(board.get_data()):
            if str(v) == "_":
                valid_moves.append(i)
        if valid_moves:
            move = random.choice(valid_moves)
            collumn, row = board.get_collumn_row_at_index(move)
        return collumn, row

    def __get_highest_threat(self, threats):
        """To be used internally in the class only. """
        threat_to_tackle = []
        max_threat = 0
        for i in threats:
            threat_level = i[0][2]
            if threat_level > max_threat:
                threat_to_tackle = i
                max_threat = threat_level
        return threat_to_tackle

    def get_move(self):
        """Calculates a move"""
        board = self._board
        collumn, row = -1, -1
        threats = self.get_threats(board.get_rows_to_win() - 2, False)
        threat_to_tackle = self.__get_highest_threat(threats)
        # for now, I haven't implemented the bot "attacking", so it will just go a random move when it doesn't need to defend.
        if not threats:
            collumn, row = self.get_random_move()
        else: # threats found, go defensive. 
            while True:
                if not threat_to_tackle:
                    collumn, row = self.get_random_move()
                    break
                print(threat_to_tackle)
                collumn0, row0 = threat_to_tackle[0][0][0], threat_to_tackle[0][0][1]
                collumn1, row1 = threat_to_tackle[1][0][0], threat_to_tackle[1][0][1]
                adj_marker_0, _ = board.get_marker_at_position(collumn0, row0)
                adj_marker_1, _ = board.get_marker_at_position(collumn1, row1)

                if adj_marker_1 != self._marker and adj_marker_0 != self._marker:
                    move0 = (collumn0 + threat_to_tackle[0][1][0], row0 + threat_to_tackle[0][1][1])
                    move1 = (collumn1 + threat_to_tackle[1][1][0], row1 + threat_to_tackle[1][1][1])
                    move_chosen = 1
                    print("Possible moves: ", move0, move1)
                    if str(adj_marker_1) != "_" and adj_marker_1 != self._marker:
                        collumn, row = move0[0], move0[1]
                        move_chosen = 0
                    else:
                        collumn, row = move1[0], move1[1]
                        move_chosen = 1
                    try:
                        print("Attempting to play:", collumn, row)
                        occupied, _ = board.get_marker_at_position(collumn, row)
                        if str(occupied) != "_": # if move chosen is occupied, go other side
                            print("Bot tried to play in non-empty space")
                            if move_chosen == 0:
                                collumn, row = move1[0], move1[1]
                            else:
                                collumn, row = move0[0], move0[1]
                            occupied, _ = board.get_marker_at_position(collumn, row) # if both moves occupied, should mean threat blocked.
                            if str(occupied) != "_":
                                print("Bot still tried to play in non-empty space")
                                collumn, row = -1, -1
                                # collumn, row = self.get_random_move()
                            else:
                                break
                    except IndexError:
                        print("Bot tried to play outside the board")
                        try:
                            if move_chosen == 0:
                                collumn, row = move1[0], move1[1]
                            else:
                                collumn, row = move0[0], move0[1]
                            occupied, _ = board.get_marker_at_position(collumn, row) # if both moves occupied, attack instead.
                            if str(occupied) != "_":
                                print("Bot tried to play in non-empty space")
                                collumn, row = -1, -1
                                # collumn, row = self.get_random_move()
                        except IndexError:
                            collumn, row = -1, -1
                        # collumn, row = self.get_random_move()
                        # break
                if collumn + row == -2:
                    threats.remove(threat_to_tackle) # if chain completely blocked, remove the threat and search for a different one.
                    threat_to_tackle = self.__get_highest_threat(threats)
                elif not threats:
                    print("Options exhausted.")
                    collumn, row = self.get_random_move() # if all threats blocked, go random move/attack
                    break
                else:
                    break
        print("Bot plays:", collumn, row)
        return collumn, row
        

class DumbBot(Bot):
    def __init__(self, marker: str, board: Board) -> None:
        super().__init__(marker, board)
    
    def get_move(self):
        return self.get_random_move()



game_board = Board(5, 5, 4)
player = Player("O", game_board)
bot = Bot("X", game_board)
# in theory the 'smarter' bot should win against the dumb bot. 

print(game_board)
while True:
    time.sleep(1)
    try:
        player.apply_move()
    except IndexError:
        print("Draw")
        break
    print(game_board)
    if game_board.check_win() == player.get_marker():
        print(game_board)
        print(player.get_marker(), "wins!")
        break
    else:
        pass
    time.sleep(1)
    try:
        bot.apply_move()
    except IndexError:
        print("Draw")
        break
    print(game_board)
    if game_board.check_win() == bot.get_marker():
        print(game_board)
        print(bot.get_marker(), "wins!")
        break
    else:
        pass

