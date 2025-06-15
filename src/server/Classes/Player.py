from .Game import Game
from Enum import Rank, Suit
import struct

class Player:
    
    def __init__(self, player_id):
        """Initialize player with an ID and an empty hand."""
        self.player_id = player_id
        self.hand = []
        # deck? 

    def draw(self, game):
        """Draw a card from the deck."""
        card = game.draw_card()
        if card:
            self.hand.append(card)

    def play_card(self, card_index):
        """Play a card from the player's hand."""
        if 0 <= card_index < len(self.hand):
            return self.hand.pop(card_index)
        return None
    
    def draw_cards(self, game, count=5):
        for _ in range(count):
            self.draw(game)
        """Draw `count` cards from the deck and add them to the player's hand."""

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
                    print(f"Card {card} is allowed due to penalty")
            if no_cards_can_defend and draw_deck:
                self.draw_cards(game, game.penalty - 1)
                game.penalty = 0
            else:
                return self.hand
       
        for card in self.hand:
            if card.suit == top_card.suit or card.rank == top_card.rank:
                card.allowed = True
                print(f"Card {card} is allowed")
            else:
                card.allowed = False
        return self.hand
    
    def delete_card_from_hand(self,game, card_to_remove):
        """Remove a card from the player's hand."""
        # print(f"Deleting card {card_to_remove.color}-{card_to_remove.value} from hand")
        for card in self.hand:
            if card.rank == card_to_remove.rank and card.suit == card_to_remove.suit:
                game.top_card = card_to_remove
                self.hand.remove(card)
                break
   
    def to_binary_with_game_info(self, game,your_turn,draw_card_allowed=True):
        data = bytearray()
        data.extend(struct.pack("<H", game.game_id))         # 2 bajty TODO odwrotnie trzeba to zrobic
        data.append(self.player_id)                       # 1 bajt
        data.append(len(self.hand))                       # 1 bajt
        data.append(your_turn)                            # 1 bajt - TODO: to change this is allowed filed
        data.append(draw_card_allowed)                  # 1 bajt - TODO: to change this is allowed filed
        data.append(game.top_card.rank.value)
        data.append(game.top_card.suit.value)
        data.append(game.top_card.allowed)
                                # 1 bajt - TODO: to change this is allowed filed
     
        for card in self.hand:
            data.append(card.rank.value)
            data.append(card.suit.value)
            data.append(card.allowed) #TODO to change this is allowed filed
        
        return bytes(data)
