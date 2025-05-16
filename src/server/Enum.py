from enum import Enum

class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

class Suit(Enum):
    HEARTS = 0
    DIAMONDS = 1
    CLUBS = 2
    SPADES = 3

class Action(Enum):
    FIRST_PLAYER_INITIALIZATION = 0
    SECOND_PLAYER_INITIALIZATION = 1
    PLAYER_CLICK = 2

