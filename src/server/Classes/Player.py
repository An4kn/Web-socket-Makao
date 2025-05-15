from .Game import Game
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
   
    def to_binary_with_game_info(self, game_id):
        data = bytearray()
        data.extend(struct.pack("<H", game_id))           # 2 bajty
        data.append(self.player_id)                       # 1 bajt
        data.append(len(self.hand))                       # 1 bajt

        for card in self.hand:
            data.append(card.rank.value)
            data.append(card.suit.value)
            data.append(card.action.value)
            # print(f"Card: {card}, Rank Value: {card.rank.value}, Suit Value: {card.suit.value}, Action Value: {card.action.value}")
        return bytes(data)

    # def _get_rank_value(self, rank):
    #     ranks_map = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
    #     return ranks_map.get(rank, 0)

    # def _get_suit_value(self, suit):
    #     suits_map = {"Hearts": 0, "Diamonds": 1, "Clubs": 2, "Spades": 3}
    #     return suits_map.get(suit, 0)

    # def _get_action_value(self, action):
    #     actions_map = {None: 0, "skip": 1, "reverse": 2, "draw 2": 3}
    #     return actions_map.get(action, 0)

    # def to_binary_with_game_info(self, game_id):
    #     """Konwertuje obiekt Player i info o grze na binarną reprezentację."""
    #     game_id_binary = struct.pack("<H", game_id)
    #     player_id_binary = struct.pack("<B", self.player_id)
    #     hand_size = len(self.hand)
    #     hand_size_binary = struct.pack("<B", hand_size)
    #     hand_binary = b""
    #     for card in self.hand:
    #         rank_value = self._get_rank_value(card.rank)
    #         suit_value = self._get_suit_value(card.suit)
    #         action_value = self._get_action_value(card.action)
    #         print(f"Card: {card}, Rank Value: {rank_value}, Suit Value: {suit_value}, Action Value: {action_value}")
    #         card_binary = struct.pack("<BBB", rank_value, suit_value, action_value)
    #         hand_binary += card_binary
    #     return game_id_binary + player_id_binary + hand_size_binary + hand_binary
