#Skeleton Program code for the AQA A Level Paper 1 Summer 2024 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.9.4 programming environment

from __future__ import annotations
import random
import os


def reverse_rows(array: list, width: int):
    array_copy = array.copy()
    for i in range(width):
        for j in range(width):
            index = i * width + j
            new_index = i * width + width - j - 1
            array_copy[new_index] = array[index] 
    return array_copy


def transpose(array: list, width: int):
    array_copy = array.copy()
    for i in range(width):
        # iterating through rows
        for j in range(width):
            index = j * width + i
            new_index = i * width + j
            array_copy[new_index] = array[index]
    return array_copy


def rotate_90(array: list, width: int):
    array = transpose(array, width)
    array = reverse_rows(array, width)
    return array


def Main():
    Again = "y"
    Score = 0
    while Again == "y":
        Filename = input("Press Enter to start a standard puzzle or enter name of file to load: ")
        if len(Filename) > 0:
            MyPuzzle = Puzzle(Filename + ".txt")
        else:
            MyPuzzle = Puzzle(8, int(8 * 8 * 0.6))
        Score = MyPuzzle.AttemptPuzzle()
        print("Puzzle finished. Your score was: " + str(Score))
        Again = input("Do another puzzle? ").lower()


class Puzzle():
    def __init__(self, *args):
        self.__MoveHistory = []

        if len(args) == 1:
            self.__Score = 0
            self.__SymbolsLeft = 0
            self.__GridSize = 0
            self.__Grid = []
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            self.__LoadPuzzle(args[0])
        else:
            self.__Score = 0
            self.__SymbolsLeft = args[1]
            self.__GridSize = args[0]
            self.__Grid = []
            for Count in range(1, self.__GridSize * self.__GridSize + 1):
                if random.randrange(1, 101) < 90:
                    C = Cell()
                else:
                    C = BlockedCell()
                self.__Grid.append(C)
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            QPattern = Pattern("Q", "QQ**Q**QQ")
            self.__AllowedPatterns.append(QPattern)
            self.__AllowedSymbols.append("Q")
            XPattern = Pattern("X", "X*X*X*X*X")
            self.__AllowedPatterns.append(XPattern)
            self.__AllowedSymbols.append("X")
            TPattern = Pattern("T", "TTT**T**T")
            self.__AllowedPatterns.append(TPattern)
            self.__AllowedSymbols.append("T")
            CPattern = Pattern("C", "CCC*CCCC*")
            self.__AllowedPatterns.append(CPattern)
            self.__AllowedSymbols.append("C")

        self.__AllowedSymbols.append("#")

    def __LoadPuzzle(self, Filename):
        try:
            with open(Filename) as f:
                data = f.read()
                self.DeSerialise(data)
        except FileNotFoundError:
            print("Puzzle not loaded")
    
    def DeSerialise(self, data: str):
        # resetting everything
        self.__AllowedSymbols = []
        self.__AllowedPatterns = []
        self.__Grid = []

        lines = data.split("\n")
        current_line = 0
        
        num_of_symbols = int(lines[current_line].rstrip())
        current_line += 1
        for i in range(current_line, current_line + num_of_symbols):
            current_line += 1
            self.__AllowedSymbols.append(lines[i])
        num_of_patterns = int(lines[current_line])
        current_line += 1
        for i in range(current_line, current_line + num_of_patterns):
            current_line += 1
            items = lines[i].rstrip().split(",")
            pattern = Pattern(items[0], items[1])
            self.__AllowedPatterns.append(pattern)
        self.__GridSize = int(lines[current_line].rstrip())
        current_line += 1
        for i in range(current_line, current_line + self.__GridSize * self.__GridSize):
            current_line += 1
            items = lines[i].rstrip().split(",")
            if items[0]  == "@":
                self.__Grid.append(BlockedCell())
            else:
                cell = Cell()
                cell.ChangeSymbolInCell(items[0])
                for symbol in range(1, len(items)):
                    cell.AddToNotAllowedSymbols(items[symbol])
                self.__Grid.append(cell)
        self.__Score = int(lines[current_line].rstrip())
        current_line += 1
        self.__SymbolsLeft = int(lines[current_line].rstrip())


    def Serialise(self):
        data = ""
        # number of allowed symbols
        data += str(len(self.__AllowedSymbols)) + "\n" 

        # the allowed symbols
        for i in self.__AllowedSymbols:
            data += i + "\n"

        # number of allowed patterns
        data += str(len(self.__AllowedPatterns)) + "\n"
    
        # the allowed patterns. "C", "CC".. etc.
        for i in self.__AllowedPatterns:
            data += i.GetPatternSymbol() + "," + i.GetPatternSequence() + "\n"

        data += str(self.__GridSize) + "\n"
        
        # the grid data information. 
        for i in self.__Grid:
            data += i._Symbol + "," + ",".join(i.GetNotAllowedSymbols()) + "\n"
        
        data += str(self.__Score) + "\n"
        data += str(self.__SymbolsLeft)

        return data
    
    def CacheMove(self, data):
        length = len(self.__MoveHistory) 
        if length == 5:
            self.__MoveHistory.pop()
        self.__MoveHistory.append(data)
    
    def Undo(self):
        data = self.__MoveHistory.pop()
        self.DeSerialise(data)
        return 

    def GetSaveLocation(self):
        path = input("What should the file be called? ") + ".txt"
        file = open(path, "w")
        return file

    
    def Save(self):
        data = self.Serialise()
        file = self.GetSaveLocation()
        file.write(data)
        file.close()
    

    def AttemptPuzzle(self):
        Finished = False
        while not Finished:
            puzzle_data = self.Serialise()
            self.CacheMove(puzzle_data)
            self.DisplayPuzzle()
            print("Current score: " + str(self.__Score))
            print("Symbols left: " + str(self.__SymbolsLeft))
            Row = -1
            Column = -1
            Valid = False
            while not Valid:
                try:
                    Row = int(input("Enter row number: "))
                    if Row > self.__GridSize or Row <= 0:
                        continue
                    Column = int(input("Enter column number: "))
                    if Column > self.__GridSize or Column <= 0:
                        continue
                    Valid = True
                except ValueError:
                    pass
            Symbol = self.__GetSymbolFromUser()
            self.__SymbolsLeft -= 1
            CurrentCell = self.__GetCell(Row, Column)
            if CurrentCell.CheckSymbolAllowed(Symbol):

                if Symbol == "#":
                    # we can just change the symbol in the cell to ""
                    # internally that is the 'empty' symbol. 
                    self.__SetCell(Row, Column, Cell())
                    self.__Score -= 3
                else:
                    CurrentCell.ChangeSymbolInCell(Symbol)
                    AmountToAddToScore = self.CheckforMatchWithPattern(Row, Column)
                    if AmountToAddToScore > 0:
                        self.__Score += AmountToAddToScore

                # save data
                reply = "y"

                data = self.Serialise()

                while reply == "y":
                    reply = input("undo? ").lower()
                    if reply == "y":
                        self.Undo()

                self.CacheMove(data)

                reply = input("Save? ").lower()
                if reply == "y":
                    self.Save()

            if self.__SymbolsLeft == 0:
                Finished = True
        print()
        self.DisplayPuzzle()
        print()
        return self.__Score

    def __SetCell(self, Row, Column, Cell: Cell):
        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
        self.__Grid[Index] = Cell

    def __GetCell(self, Row, Column):
        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
        if Index >= 0:
            return self.__Grid[Index]
        else:
            raise IndexError()

    def CheckforMatchWithPattern(self, Row, Column):
        for StartRow in range(Row + 2, Row - 1, -1):
            for StartColumn in range(Column - 2, Column + 1):
                try:
                    PatternString = ""
                    PatternString += self.__GetCell(StartRow, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 1).GetSymbol()
                    for P in self.__AllowedPatterns:
                        CurrentCell = self.__GetCell(Row, Column)
                        CurrentSymbol = CurrentCell.GetSymbol()
                        if not CurrentCell.CheckSymbolAllowed(CurrentSymbol):
                            continue
                        
                        no_rotation = rotate_90(list(PatternString), 3)
                        rotation_90 = rotate_90(no_rotation, 3)
                        rotation_180 = rotate_90(rotation_90, 3)
                        rotation_270 = rotate_90(rotation_180, 3)

                        for rotated_pattern in [no_rotation, rotation_90, rotation_180, rotation_270]:
                            rotated_pattern = "".join(rotated_pattern)
                            if P.MatchesPattern(rotated_pattern, CurrentSymbol):
                                self.__GetCell(StartRow, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                                self.__GetCell(StartRow, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                                self.__GetCell(StartRow, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                                self.__GetCell(StartRow - 1, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                                self.__GetCell(StartRow - 2, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                                self.__GetCell(StartRow - 2, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                                self.__GetCell(StartRow - 2, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                                self.__GetCell(StartRow - 1, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                                self.__GetCell(StartRow - 1, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                                return 10
                except IndexError:
                    pass
        return 0

    def __GetSymbolFromUser(self):
        Symbol = ""
        while not Symbol in self.__AllowedSymbols:
            Symbol = input("Enter symbol: ")
        return Symbol

    def __CreateHorizontalLine(self):
        Line = "  "
        for Count in range(1, self.__GridSize * 2 + 2):
            Line = Line + "-"
        return Line

    def DisplayPuzzle(self):
        print()
        if self.__GridSize < 10:
            print("  ", end='')
            for Count in range(1, self.__GridSize + 1):
                print(" " + str(Count), end='')
        print()
        print(self.__CreateHorizontalLine())
        for Count in range(0, len(self.__Grid)):
            if Count % self.__GridSize == 0 and self.__GridSize < 10:
                print(str(self.__GridSize - ((Count + 1) // self.__GridSize)) + " ", end='')
            print("|" + self.__Grid[Count].GetSymbol(), end='')
            if (Count + 1) % self.__GridSize == 0:
                print("|")
                print(self.__CreateHorizontalLine())

class Pattern():
    def __init__(self, SymbolToUse, PatternString):
        self.__Symbol = SymbolToUse
        self.__PatternSequence = PatternString

    def GetPatternSymbol(self):
        return self.__Symbol

    def MatchesPattern(self, PatternString, SymbolPlaced: str):
        if SymbolPlaced != self.__Symbol:
            return False
        for Count in range(0, len(self.__PatternSequence)):
            try:
                if self.__PatternSequence[Count] == self.__Symbol:
                    if PatternString[Count] != self.__Symbol:
                        return False
                elif PatternString[Count] == self.__Symbol:
                    return False
            except Exception as ex:
                print(f"EXCEPTION in MatchesPattern: {ex}")
        return True

    def GetPatternSequence(self):
      return self.__PatternSequence

class Cell():
    def __init__(self):
        self._Symbol = ""
        self._Checked = False
        self.__SymbolsNotAllowed = []

    def CellChecked(self):
        return self._Checked

    def GetSymbol(self):
        if self.IsEmpty():
          return "-"
        else:
          return self._Symbol
    
    def IsEmpty(self):
        if len(self._Symbol) == 0:
            return True
        else:
            return False

    def ChangeSymbolInCell(self, NewSymbol):
        self._Symbol = NewSymbol

    def CheckSymbolAllowed(self, SymbolToCheck: str):
        for Item in self.__SymbolsNotAllowed:
            if Item == SymbolToCheck:
                return False
        return True
    
    def GetNotAllowedSymbols(self):
        return self.__SymbolsNotAllowed

    def AddToNotAllowedSymbols(self, SymbolToAdd: str):
        self.__SymbolsNotAllowed.append(SymbolToAdd)

    def UpdateCell(self):
        pass

class BlockedCell(Cell):
    def __init__(self):
        super(BlockedCell, self).__init__()
        self._Symbol = "@"

    def CheckSymbolAllowed(self, SymbolToCheck):
        return SymbolToCheck == "#"

if __name__ == "__main__":
    Main()