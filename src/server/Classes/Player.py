from .Game import Game
from Enum import Rank, Suit
import struct

class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.hand = []

    def draw(self, game):
        card = game.draw_card()
        if card:
            self.hand.append(card)

    def play_card(self, card_index):
        if 0 <= card_index < len(self.hand):
            return self.hand.pop(card_index)
        return None
    
    def draw_cards(self, game, count=5):
        for _ in range(count):
            self.draw(game)

    def set_playable_cards(self,game,draw_deck=False):
        top_card = game.top_card
        no_cards_can_defend = True
        if game.penalty > 0:
            for card in self.hand:
                if card.rank.value == 2 or card.rank.value == 3 or (card.rank.value == Rank.KING and card.suit in [Suit.SPADES, Suit.HEARTS]):
                    card.allowed = True
                    no_cards_can_defend = False
                else:
                    card.allowed = False
            if no_cards_can_defend and draw_deck:
                self.draw_cards(game, game.penalty - 1)
                game.penalty = 0
            else:
                return self.hand
       
        for card in self.hand:
            if card.suit == top_card.suit or card.rank == top_card.rank:
                card.allowed = True
            else:
                card.allowed = False
        return self.hand
    
    def delete_card_from_hand(self,game, card_to_remove):
        for card in self.hand:
            if card.rank == card_to_remove.rank and card.suit == card_to_remove.suit:
                game.top_card = card_to_remove
                self.hand.remove(card)
                break
   
    def to_binary_with_game_info(self, game,your_turn,draw_card_allowed=True):
        data = bytearray()
        data.extend(struct.pack("<H", game.game_id))
        data.append(self.player_id)
        data.append(len(self.hand))
        data.append(your_turn)                           
        data.append(draw_card_allowed)
        data.append(game.top_card.rank.value)
        data.append(game.top_card.suit.value)
        data.append(game.top_card.allowed)
     
        for card in self.hand:
            data.append(card.rank.value)
            data.append(card.suit.value)
            data.append(card.allowed)
        
        return bytes(data)
