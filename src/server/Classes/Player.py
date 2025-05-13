from server.Classes.Game import Game

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
        
