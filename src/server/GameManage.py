# import server.Classes.Game as Game
from Classes.Game import Game
# import Game"???
# from .Classes.GameManager import GameManager
from Classes.Player import Player


def ManageGame(players, games, player_id=-1,game_id=-1,init_game=True): # moze id -1??
    #trzeba sprawdzic czy ninicjalizacja?????
    if init_game: #to juz po inizjalizacji gra się zaczyna
        #to jest po rozpoczęciu gry
        game, player = FindGame(games, players)
        game.init_top_card()
        player.set_playable_cards(game.top_card)
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
    
    player = Add_player(players, game) 
    
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

def Add_player(players, game):
    player_id = max(players.keys(), default=0) + 1
    player = Player(player_id)
    players[player_id] = player # tutaj chyba append?
        
    game.add_player(player)
    player.draw_cards(game, 5)
    return player

# def CreateUserID():
#     game1 = game_manager.create_game(1)
