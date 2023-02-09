# Skeleton Program code for the AQA A Level Paper 1 2018 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA Programmer Team
# developed using Python 3.5.1

import random
import json

class QueueOfTiles():
  def __init__(self, max_size: int) -> None:
    self._queue = [None] * max_size
    self._front = -1
    self._rear = -1
    self._index = 0
    self._max_size = max_size
    for _ in range(max_size):
      self.add_random_letter()

  def pop(self):
    """Returns the item at the front of the queue"""
    if self.is_empty(): raise IndexError("Queue empty")
    item = self._queue[self._front]
    if self._front == self._rear:
      self._front = -1
      self._rear = -1
    else:
      self._front = (self._front + 1) % self._max_size
    self._index = self._front
    return item

  def add_random_letter(self):
    """Wrapper for .append to add a random character to the queue"""
    self.append(chr(65 + random.randint(0, 25)))

  def append(self, item):
    """Adds item to the end of the queue"""
    if self.is_full(): raise IndexError("Queue full")
    self._index = self._front
    if self.is_empty():
      self._front = 0
      self._rear = 0
    else:
      self._rear = (self._rear + 1) % self._max_size
    self._queue[self._rear] = item

  def __iter__(self):
    return self
  
  def __next__(self):
    if self.is_empty(): raise StopIteration
    if self._index + 1 == self._rear: raise StopIteration
    self._index = (self._index + 1) % self._max_size
    return self._queue[self._index]

  def show(self):
    """Prints out the contents of the queue"""
    for i in self:
      print(i, end="")
    print()

  def is_empty(self):
    return self._rear == -1 and self._front == -1
  
  def is_full(self):
    return (self._rear + 1) % self._max_size == self._front


class TextValues():
  def __init__(self) -> None:
    self.letter_frequency = [None] * 26
    self.letter_scores = {}

    # counting the number of each letter in the text file.
    with open("C://Users//Yacco//VSCodeSt//aqa_preliminary//aqawords.txt", "r") as f:
      text = f.read()
      for i, v in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        self.letter_frequency[i] = text.count(v)

    self.letter_count = sum(self.letter_frequency)

    for i, v in enumerate(self.letter_frequency):
      score = self.get_score_for_word(v)
      self.letter_scores[chr(65 + i)] = score

  def get_character_from_index(index: int):
    """Returns the alphabetic character from its ordinal position in the alphabet"""
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[index]

  def get_score_for_word(self, word: str) -> int:
    return max([int((self.letter_count / word) / 5), 1])
  
  def get_highest_score(self, word_list: list):
    max_score = 0
    for i in word_list:
      pass

    
def DisplayTileValues(TileData: TextValues, AllowedWords):
  print()
  print("TILE VALUES")
  print()  
  for Letter, Points in TileData.letter_scores.items():
    print("Points for " + Letter + ": " + str(Points))
  print()

def GetStartingHand(TileQueue, StartHandSize):
  Hand = ""
  for Count in range(StartHandSize):
    Hand += TileQueue.pop()
    TileQueue.append()
  return Hand

def LoadAllowedWords():
  AllowedWords = []
  WordsFile = open(r"C://Users//Yacco//VSCodeSt//aqa_preliminary//aqawords.txt", "r") # removed try and except so FileNotFoundError
  for Word in WordsFile:
    AllowedWords.append(Word.strip().upper())
  WordsFile.close()
  return AllowedWords

def CheckWordIsInTiles(Word, PlayerTiles):
  InTiles = True
  CopyOfTiles = PlayerTiles
  for Count in range(len(Word)):
    if Word[Count] in CopyOfTiles:
      CopyOfTiles = CopyOfTiles.replace(Word[Count], "", 1)
    else:
      InTiles = False
  return InTiles 

def CheckWordIsValid(word: str, allowed_words: list) -> bool:
    """Recursively binary searches through a SORTED list"""
    upper_bound = len(allowed_words)
    middle = (upper_bound // 2)
    middle_word = allowed_words[middle]
    if middle_word == word:
        return True
    elif upper_bound <= 1:
        return False
    if word > middle_word:
        allowed_words = allowed_words[middle:upper_bound]
        return CheckWordIsValid(word, allowed_words)
    else:
        upper_bound = middle
        allowed_words = allowed_words[0:middle]
        return CheckWordIsValid(word, allowed_words)

def AddEndOfTurnTiles(TileQueue, PlayerTiles, NewTileChoice, Choice):
  if NewTileChoice == "1":
    NoOfEndOfTurnTiles = len(Choice)
  elif NewTileChoice == "2":
    NoOfEndOfTurnTiles = 3    
  else:
    NoOfEndOfTurnTiles = len(Choice) + 3
  for Count in range(NoOfEndOfTurnTiles):
    PlayerTiles += TileQueue.pop()
    TileQueue.append()
  return TileQueue, PlayerTiles  

def FillHandWithTiles(TileQueue, PlayerTiles, MaxHandSize):
  while len(PlayerTiles) <= MaxHandSize:
    PlayerTiles += TileQueue.pop()
    TileQueue.append()
  return TileQueue, PlayerTiles  

def GetScoreForWord(Word, TileData: TextValues):
  Score = 0
  for i in Word:
    Score += TileData.letter_scores[i]
  if len(Word) > 7:
    Score += 20
  elif len(Word) > 5:
    Score += 5
  return Score
  
def UpdateAfterAllowedWord(Word, PlayerTiles, PlayerScore, PlayerTilesPlayed, TileData: TextValues, AllowedWords):
  PlayerTilesPlayed += len(Word)
  for Letter in Word:
    PlayerTiles = PlayerTiles.replace(Letter, "", 1)
  PlayerScore += GetScoreForWord(Word, TileData)
  return PlayerTiles, PlayerScore, PlayerTilesPlayed
      
def UpdateScoreWithPenalty(PlayerScore, PlayerTiles, TileData: TextValues):
  for i in PlayerTiles:
    PlayerScore -= TileData.letter_scores[i]
  return PlayerScore

def GetChoice(is_bot: bool):
  print()
  print("Either:")
  print("     enter the word you would like to play OR")
  print("     press 1 to display the letter values OR")
  print("     press 4 to view the tile queue OR")
  print("     press 7 to view your tiles again OR")
  print("     press 0 to fill hand and stop the game.")
  if is_bot:
    Choice = ""
  else:
    Choice = input(">")
    Choice = Choice.upper()
  print()
  
  return Choice

def GetNewTileChoice():
  NewTileChoice = ""
  while NewTileChoice not in ["1", "2", "3", "4"]:
    print("Do you want to:")
    print("     replace the tiles you used (1) OR")
    print("     get three extra tiles (2) OR")
    print("     replace the tiles you used and get three extra tiles (3) OR")
    print("     get no new tiles (4)?")
    NewTileChoice = input(">")
  return NewTileChoice

def DisplayTilesInHand(PlayerTiles):
  print()
  print("Your current hand:", PlayerTiles)
  
def HaveTurn(PlayerName, PlayerTiles, PlayerTilesPlayed, PlayerScore, TileData: TextValues, TileQueue, AllowedWords, MaxHandSize, NoOfEndOfTurnTiles, IsBot: bool):
  print()
  print(PlayerName, "it is your turn.")
  DisplayTilesInHand(PlayerTiles)
  NewTileChoice = "2"
  ValidChoice = False
  while not ValidChoice:
    Choice = GetChoice(IsBot)
    if Choice == "1":
      DisplayTileValues(TileData, AllowedWords)
    elif Choice == "4":
      TileQueue.Show()
    elif Choice == "7":
      DisplayTilesInHand(PlayerTiles)      
    elif Choice == "0":
      ValidChoice = True
      TileQueue, PlayerTiles = FillHandWithTiles(TileQueue, PlayerTiles, MaxHandSize)
    else:
      ValidChoice = True
      if len(Choice) == 0:
        ValidWord = False
      else:
        ValidWord = CheckWordIsInTiles(Choice, PlayerTiles)
      if ValidWord:
        ValidWord = CheckWordIsValid(Choice, AllowedWords)
        if ValidWord:
          print()
          print("Valid word")
          print()
          PlayerTiles, PlayerScore, PlayerTilesPlayed = UpdateAfterAllowedWord(Choice, PlayerTiles, PlayerScore, PlayerTilesPlayed, TileData, AllowedWords)
          NewTileChoice = GetNewTileChoice()
      if not ValidWord:
        print()
        print("Not a valid attempt, you lose your turn.")
        print()
      if NewTileChoice != "4":
        TileQueue, PlayerTiles = AddEndOfTurnTiles(TileQueue, PlayerTiles, NewTileChoice, Choice)
      print()
      print("Your word was:", Choice)
      print("Your new score is:", PlayerScore)
      print("You have played", PlayerTilesPlayed, "tiles so far in this game.")
  return PlayerTiles, PlayerTilesPlayed, PlayerScore, TileQueue  

def DisplayWinner(PlayerOneScore, PlayerTwoScore, PlayerOneName, PlayerTwoName):
  print()
  print("**** GAME OVER! ****")
  print()
  print(PlayerOneName, "your score is", PlayerOneScore)
  print(PlayerTwoName, "your score is", PlayerTwoScore)
  if PlayerOneScore > PlayerTwoScore:
    print(PlayerOneName, "wins!")
  elif PlayerTwoScore > PlayerOneScore:
    print(PlayerTwoName, "wins!")
  else:
    print("It is a draw!")
  print()
  
def PlayGame(AllowedWords, TileData: TextValues, RandomStart, StartHandSize, MaxHandSize, MaxTilesPlayed, NoOfEndOfTurnTiles):
  PlayerOneName = input("Player one's name >")
  PlayerTwoName = input("Player two's name >")
  PlayerOneScore = 50
  PlayerTwoScore = 50
  PlayerOneTilesPlayed = 0
  PlayerTwoTilesPlayed = 0
  TileQueue = QueueOfTiles(20, TileData.letter_frequency)
  if RandomStart:
    PlayerOneTiles = GetStartingHand(TileQueue, StartHandSize)
    PlayerTwoTiles = GetStartingHand(TileQueue, StartHandSize)
  else:
    PlayerOneTiles = "BTAHANDENONSARJ"
    PlayerTwoTiles = "CELZXIOTNESMUAA"
  while PlayerOneTilesPlayed <= MaxTilesPlayed and PlayerTwoTilesPlayed <= MaxTilesPlayed and len(PlayerOneTiles) < MaxHandSize and len(PlayerTwoTiles) < MaxHandSize:
    PlayerOneTiles, PlayerOneTilesPlayed, PlayerOneScore, TileQueue = HaveTurn(PlayerOneName, PlayerOneTiles, PlayerOneTilesPlayed, PlayerOneScore, TileData, TileQueue, AllowedWords, MaxHandSize, NoOfEndOfTurnTiles, False)
    print()
    input("Press Enter to continue")
    print()
    PlayerTwoTiles, PlayerTwoTilesPlayed, PlayerTwoScore, TileQueue = HaveTurn(PlayerTwoName, PlayerTwoTiles, PlayerTwoTilesPlayed, PlayerTwoScore, TileData, TileQueue, AllowedWords, MaxHandSize, NoOfEndOfTurnTiles, True)
  PlayerOneScore = UpdateScoreWithPenalty(PlayerOneScore, PlayerOneTiles, TileData)
  PlayerTwoScore = UpdateScoreWithPenalty(PlayerTwoScore, PlayerTwoTiles, TileData)
  DisplayWinner(PlayerOneScore, PlayerTwoScore, PlayerOneName, PlayerTwoName)

def DisplayMenu():
  print()
  print("=========")
  print("MAIN MENU")
  print("=========")
  print()
  print("1. Play game with random start hand")
  print("2. Play game with training start hand")
  print("3. View high scores")
  print("9. Quit")
  print()
  
def Main():
  print("++++++++++++++++++++++++++++++++++++++")
  print("+ Welcome to the WORDS WITH AQA game +")
  print("++++++++++++++++++++++++++++++++++++++")
  print()
  print()
  AllowedWords = LoadAllowedWords()
  TileData = TextValues()
  MaxHandSize = 20
  MaxTilesPlayed = 50
  NoOfEndOfTurnTiles = 3
  StartHandSize = 15
  Choice = ""
  while Choice != "9":
    DisplayMenu()
    Choice = input("Enter your choice: ")
    if Choice == "1":
      PlayGame(AllowedWords, TileData, True, StartHandSize, MaxHandSize, MaxTilesPlayed, NoOfEndOfTurnTiles)
    elif Choice == "2":
      PlayGame(AllowedWords, TileData, False, 15, MaxHandSize, MaxTilesPlayed, NoOfEndOfTurnTiles)
      
if __name__ == "__main__":
  Main()
