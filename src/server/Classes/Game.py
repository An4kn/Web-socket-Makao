import random
from .Card import Card
from Enum import Rank, Suit, Client_send_action



class Game:
    def __init__(self, game_id, max_players=2):
        """Initializes the game with up to `max_players` players."""
        self.game_id = game_id
        self.max_players = max_players
        self.players = []
        self.deck = []  # Create and shuffle deck
        self.current_player = 0
        self.played_cards = []  # Stack of played cards
        self.game_over = False
        self.current_player_id = 0
        self.game_is_ready = False
        self.top_card = None
        self.battle_count = 0

    def add_player(self, player):
        """Adds a player to the game."""
        if len(self.players) < self.max_players:
            self.players.append(player)
            if len(self.players) == self.max_players:
                self.game_is_ready = True
            return True
        return False

    def start_game(self):
        """Starts the game by dealing cards to players."""
        self.deck.shuffle()
        for player in self.players:
            for _ in range(7):  # Each player gets 7 cards
                player.draw(self.deck)
        
        # Place an initial card
        self.played_cards.append(self.deck.draw_card())
  
    def create_deck(self):
        for suit in Suit:
            for rank in Rank:
                card = Card(rank=rank, suit=suit, allowed=False)  # lub domyślnie action=NONE
                self.deck.append(card)

        random.shuffle(self.deck)
        print("Talia kart:", self.deck)

    
    def draw_card(self):
        """Draws a card from the deck."""

        if self.deck:
            return self.deck.pop()
        else:
            raise Exception("Deck is empty") # TODO: Handle this case better

    def next_turn(self):
        """Moves to the next player's turn."""
        self.current_player = (self.current_player + 1) % len(self.players)

    def valid_play(self, player, card_index):
        """Checks if a card can be played."""
        if self.game_over:
            return False
        
        card_to_play = player.hand[card_index]
        top_card = self.played_cards[-1]
        
        # Card must match the top card either by color or value
        if card_to_play.color == top_card.color or card_to_play.value == top_card.value:
            return True
        
        return False

    def play_card(self, player, card_index):
        """Processes the card play action."""
        if self.valid_play(player, card_index):
            card_played = player.play_card(card_index)
            self.played_cards.append(card_played)
            self.next_turn()
            return True
        return False

    def is_game_over(self):
        """Checks if any player has no cards left."""
        for player in self.players:
            if len(player.hand) == 0:
                self.game_over = True
                return True
        return False
    
    def allow_card_to_play(self, card):
        """Checks if a card can be played."""
        # if self.game_over:
        #     return False #TODO maybe later
        
        top_card = self.played_cards[-1]
        
        # Card must match the top card either by color or value
        if card.suit == top_card.suit or card.rank == top_card.rank:
            return True
        
        return False
    
    def init_top_card(self):
        for card in self.deck:
            self.top_card = card
            self.deck.remove(card) #trigger do usuniecia karty z decka??
            if self.top_card.rank in [Rank.FIVE, Rank.SIX, Rank.SEVEN, Rank.EIGHT, Rank.NINE, Rank.TEN,Rank.QUEEN]:#zobaczymy czy dokonczymy implementencacje                 
                break
        print(f"Top card initialized: {self.top_card}")
        print(f"Top card initialized: {self.deck[-1]}")
    def drew_deck(self,player):
        # pl
        return self.deck.remove(self.deck[-1])



        



