from Enum import Rank, Suit, Client_send_action

class Card:
    def __init__(self, rank: Rank, suit: Suit, allowed=None):
        self.rank = rank
        self.suit = suit
        self.allowed = allowed  # Akcja specjalna, np. "skip", "reverse", "draw 2"

    def __repr__(self):
        return f"{self.rank} of {self.suit}" + (f" (Action: {self.allowed})" if self.allowed else "")
   
