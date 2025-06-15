import random
from .Card import Card
from Enum import Rank, Suit, Client_send_action



class Game:
    def __init__(self, game_id, max_players=2):
        self.game_id = game_id
        self.max_players = max_players
        self.players = []
        self.deck = []
        self.current_player = 0
        self.played_cards = []
        self.game_over = False
        self.current_player_id = 0
        self.game_is_ready = False
        self.top_card = None
        self.penalty = 0

    def add_player(self, player):
        if len(self.players) < self.max_players:
            self.players.append(player)
            if len(self.players) == self.max_players:
                self.game_is_ready = True
            return True
        return False

    def start_game(self):
        self.deck.shuffle()
        for player in self.players:
            for _ in range(7):
                player.draw(self.deck)
        
        self.played_cards.append(self.deck.draw_card())
  
    def create_deck(self):
        for suit in Suit:
            for rank in Rank:
                card = Card(rank=rank, suit=suit, allowed=False)
                self.deck.append(card)

        random.shuffle(self.deck)
        print("Talia kart:", self.deck)

    
    def draw_card(self):
        if self.deck:
            return self.deck.pop()
        else:
            self.create_deck()

    def penalty_card(self, card):
        if card.rank.value == 2:
            self.penalty += 2
        elif card.rank.value == 3:
            self.penalty += 3
        elif (card.rank.value == Rank.KING and card.suit == Suit.SPADES) or (card.rank.value == Rank.KING and card.suit == Suit.HEARTS):
            self.penalty += 5

    def next_turn(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def valid_play(self, player, card_index):
        if self.game_over:
            return False
        
        card_to_play = player.hand[card_index]
        top_card = self.played_cards[-1]
        
        if card_to_play.color == top_card.color or card_to_play.value == top_card.value:
            return True
        
        return False

    def play_card(self, player, card_index):
        if self.valid_play(player, card_index):
            card_played = player.play_card(card_index)
            self.played_cards.append(card_played)
            self.next_turn()
            return True
        return False

    def is_game_over(self):
        for player in self.players:
            if len(player.hand) == 0:
                self.game_over = True
                return True
        return False
    
    def allow_card_to_play(self, card):        
        top_card = self.played_cards[-1]
        
        if card.suit == top_card.suit or card.rank == top_card.rank:
            return True
        
        return False
    
    def init_top_card(self):
        for card in self.deck:
            self.top_card = card
            self.deck.remove(card)
            if self.top_card.rank in [Rank.FIVE, Rank.SIX, Rank.SEVEN, Rank.EIGHT, Rank.NINE, Rank.TEN,Rank.QUEEN]:#zobaczymy czy dokonczymy implementencacje                 
                break
    def drew_deck(self,player):
        return self.deck.remove(self.deck[-1])



        



