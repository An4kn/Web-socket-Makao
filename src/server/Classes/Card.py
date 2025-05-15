from Enum import Rank, Suit, Action

class Card:
    def __init__(self, rank: Rank, suit: Suit, action=None):
        self.rank = rank
        self.suit = suit
        self.action = action  # Akcja specjalna, np. "skip", "reverse", "draw 2"

    def __repr__(self):
        return f"{self.rank} of {self.suit}" + (f" (Action: {self.action})" if self.action else "")
