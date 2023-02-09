import datetime


class StockItem():
    def __init__(self, title, date_acquired) -> None:
        self.title = title
        self._on_loan = False
        self._date_acquired = date_acquired
    
    def set_loan(self):
        self._on_loan = True

    def display_details(self):
        for i, v in self.__dict__.items():
            print(i, "=", v)

class Book(StockItem):
    def __init__(self, title: str, date_acquired: datetime.date, author: str, ISBN: str):
        super().__init__(title, date_acquired)
        self.author = author
        self._ISBN = ISBN

class CD(StockItem):
    def __init__(self, title: str, date_acquired: datetime.date, artist: str, playing_time: float):
        super().__init__(title, date_acquired)
        self.artist = artist
        self._PlayingTime = playing_time


new_book = Book("Henlo world", datetime.date(2006, 1, 1), "bunger", "12938357")
new_book.set_loan()
new_book.display_details()

new_cd = CD("Human music", datetime.date(2002, 4, 26), "normal human", "856738109")
new_cd.set_loan()
new_cd.display_details()
