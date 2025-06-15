# import server.Classes.Game as Game
from Classes.Game import Game
# import Game"???
# from .Classes.GameManager import GameManager
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
    #usuniecie karty z deck players
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
    raise Exception("Second player not found") #TODO to usunac pozniej jakby cos sie stalo

def BroadcastToSendingPlayer(players, games, player_id, game_id):
    pass

def CreateCard(color, value):
    rank = Rank(value)
    suit = Suit(color)
    allowed = False
    card = Card(rank, suit,allowed)
    return card
    

def FirstConnection(players, games, yourturn,player_id=-1,game_id=-1,init_game=True): # moze id -1??
    #trzeba sprawdzic czy ninicjalizacja?????
    if init_game: #to juz po inizjalizacji gra się zaczyna
        #to jest po rozpoczęciu gry
        game, player = FindGame(games, players)
        if yourturn == 0:
            game.init_top_card()
        player.set_playable_cards(game)
        print("Ręka gracza 1:", player.hand)
        print("Karty w grze:", game.deck)
        print("Gracze w grze:", game.players)
      
        print(f"top_card ?: {game.top_card}")
    else:
        pass #TODO: handle game logic
    
    # game.add_player("Player 1")
    

    return game, player

def FindGame(games,players):
    game = None
    NewGame = True

    if games == {}:
        game = GameInit(games)
    else:
        print("Przeszlo do else znalazlo gre")
        max_id = max(games.keys())
        game = games[max_id]
        if game.game_is_ready:
            game = GameInit(games)
        else:
            print("Gra już istnieje, dodajemy gracza")
    
    player = AddPlayer(players, game) 
    
    return game, player
    # Game already exists, handle accordingly
        
def GameInit(games):
    # New game moze byc enumem tak jak reszta
    # Tworzymy nową grę o ID 1
    # id vs uuid
    # dodac flage ocxzekiwania reday gry
    game_id = max(games.keys(), default=0) + 1
    game = Game(game_id)
    games[game_id] = game
    game.create_deck()

    # dodac pewnie dwie funckje    
    # tworzymy nowy deck
    # game.add_player("Player 1")
    # game.start_game()
    return game

def AddPlayer(players, game):
    player_id = max(players.keys(), default=0) + 1
    player = Player(player_id)
    players[player_id] = player # tutaj chyba append?
        
    game.add_player(player)
    player.draw_cards(game, 5)
    return player

# def CreateUserID():
#     game1 = game_manager.create_game(1)
