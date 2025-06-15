from Classes.Game import Game
from Classes.Player import Player
from Classes.Card import Card
from Enum import Rank, Suit, Client_send_action

def GetCardFromDeck(players, games, player_id, game_id):
    player = players[player_id]
    game = games[game_id]
    player.draw_cards(game,1)
    player.set_playable_cards(game,True)
    return player, game

def PlayerCanDoAMove(player):
    for card in player.hand:
        if card.allowed:
            return True
    return False

def CreateMove(players,games,player_id, game_id, color, value,connections):
    player = players[player_id]
    game = games[game_id]
    card_to_remove = CreateCard(color, value)
    game.penalty_card(card_to_remove)
    player.delete_card_from_hand(game,card_to_remove)
    BroadcastToSecondPlayer(games, player_id, game_id,connections)

def BroadcastToSecondPlayer(games, sending_player_id, game_id, connections):
    game = games[game_id]
    player = FindSecondPlayer(games, sending_player_id, game_id)
    player.set_playable_cards(game)
    binary_data = player.to_binary_with_game_info(game,1)
    connections[player.player_id].write_message(binary_data, binary=True)
    
def FindSecondPlayer(games, player_id, game_id):
    game = games[game_id]
    for player in game.players:
        if player.player_id != player_id:
            return player

def CreateCard(color, value):
    rank = Rank(value)
    suit = Suit(color)
    allowed = False
    card = Card(rank, suit,allowed)
    return card
    
def FirstConnection(players, games, yourturn,player_id=-1,game_id=-1,init_game=True):
    game, player = FindGame(games, players)
    if yourturn == 0:
        game.init_top_card()
    player.set_playable_cards(game)
    print("Ręka gracza 1:", player.hand)
    print("Karty w grze:", game.deck)
    print("Gracze w grze:", game.players)

    return game, player

def FindGame(games,players):
    game = None
    NewGame = True

    if games == {}:
        game = GameInit(games)
    else:
        max_id = max(games.keys())
        game = games[max_id]
        if game.game_is_ready:
            game = GameInit(games)
    
    player = AddPlayer(players, game) 
    
    return game, player
        
def GameInit(games):
    game_id = max(games.keys(), default=0) + 1
    game = Game(game_id)
    games[game_id] = game
    game.create_deck()
    return game

def AddPlayer(players, game):
    player_id = max(players.keys(), default=0) + 1
    player = Player(player_id)
    players[player_id] = player
        
    game.add_player(player)
    player.draw_cards(game, 5)
    return player