import random


SUITS = [
    "Spades",
    "Hearts",
    "Diamonds",
    "Clubs"
]


VALUES = [
    "Ace",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "Joker",
    "Queen",
    "King"
]


class Card:
    """ A class to describe cards in a pack """
    def __init__(self, number: int) -> None:
        self._card_number = number

    def get_suit(self) -> str:
        """ return a string 'C', 'S', 'H', 'D' """
        return SUITS[self._card_number // 13][0]

    def get_value(self) -> str:
        """ return a string 'A'..'10', 'J', 'Q', 'K' """
        value = VALUES[self._card_number % 13 - 1]
        if value.isnumeric():
            return value
        return value[0]

    def get_short_name(self) -> str:
        """ return card name eg '10D' '8C' 'AH' """
        value = VALUES[self._card_number % 13 - 1]
        suit = SUITS[self._card_number // 13][0]
        if not value.isnumeric():
            value = value[0]
        return value + suit

    def get_long_name(self) -> str:
        """ return card name eg 'Ten of Diamonds' """
        value = VALUES[self._card_number % 13 - 1]
        suit = SUITS[self._card_number // 13]
        return value + " of " + suit


class Deck:
    """ A class to contain a pack of cards with methods for shuffling, adding or removing cards etc. """
    def __init__(self)-> None:
        self._card_list = []
        for i in range(52):
            self._card_list.append(Card(i))

    def length(self) -> int:
        """ returns the number of cards still in the deck """
        return len(self._card_list)

    def shuffle_deck(self) -> None:
        """ shuffles the cards """
        random.shuffle(self._card_list)

    def take_top_card(self) -> Card:
        """ removes the top card from the deck and returns it (as a card object) """
        return self._card_list[len(self._card_list)]


for i in range(41):
    card = Card(i)
    print(card.get_suit())
    print(card.get_value())
    print(card.get_short_name())
    print(card.get_long_name())
# deck = Deck()
# deck.shuffle_deck()
# for _ in range(deck.length()):
#     card = deck.take_top_card()
#     print(card.get_long_name())
