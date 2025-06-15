import tornado.web
import tornado.websocket
import tornado.ioloop
import struct

# Assuming ManageGame is a function in the GameManage module
from GameManage import FirstConnection, CreateMove, GetCardFromDeck, PlayerCanDoAMove,BroadcastToSecondPlayer


class EchoHandler(tornado.websocket.WebSocketHandler):

    games = {}
    players = {}
    connections = {}

    def open(self):
        pass

    def on_close(self):
        print("close")


    def on_message(self, message):
        # if len(message) != 6:
        #     print(f"Invalid message length: {len(message)} bytes")
        #     return
        print(f"Received message: {message}")
        if len(message) == 1: #initialization' #TODO dodac lokalne funckje
           
                
            # first_player_initialization = struct.unpack("B", message)
            yourturn = 0
            if len(self.players) % 2 == 0:
                print("First player initialization")
            else:
                yourturn = 1
                print("Second player initialization")
            
            print("Refreshing game and player data")

            game, player = FirstConnection(self.players, self.games,yourturn)
            self.connections[player.player_id] = self

            binary_data = player.to_binary_with_game_info(game,yourturn)
            self.write_message(binary_data, binary=True)
            
            print(f"Client connected. Player ID: {player.player_id}, Game ID: {game.game_id}, and the hand {player.hand} (sent to client)")
        if len(message) == 2:
            _, player_id = struct.unpack("BB", message)
            self.connections[player_id] = self

        if len(message) == 3: #draw card
            _,player_id, game_id = struct.unpack("BBB", message)
            print(f"Player {player_id} requested a card from game {game_id}")
            player, game = GetCardFromDeck(self.players, self.games, player_id, game_id)
            if PlayerCanDoAMove(player):
                print(f"Player {player_id} can do a move")
                binary_data = player.to_binary_with_game_info(game,1,False)
                self.write_message(binary_data, binary=True)
            else:
                binary_data = player.to_binary_with_game_info(game,0,False)
                self.write_message(binary_data, binary=True)
                BroadcastToSecondPlayer(self.games, player_id, game_id, self.connections)
            
        if len(message) == 4:
            
            player_id, game_id, color, value = struct.unpack("BBBB", message)
            CreateMove(self.players, self.games, player_id, game_id, color, value, self.connections)
            
            print(f"Player {player_id} did action , card: {color}-{value}, hand size: ")

    
    def check_origin(self, origin):#TODO po co to jest?
        return True

if __name__ == "__main__":
    app = tornado.web.Application([
        ("/ws", EchoHandler),
    ])
    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()