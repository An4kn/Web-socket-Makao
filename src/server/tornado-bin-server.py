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
        print(f"Received message: {message}")
        if len(message) == 1: 
            self.handle_first_connection()

        if len(message) == 2:
            self.handle_reconnection(message)

        if len(message) == 3:
            self.handle_draw_card_request(message)
            
        if len(message) == 4:
            self.handle_move_request(message)

    def check_origin(self, origin):
        return True

    def handle_first_connection(self):
        yourturn = 0
        if len(self.players) % 2 == 1:
            yourturn = 1

        game, player = FirstConnection(self.players, self.games, yourturn)
        self.connections[player.player_id] = self

        binary_data = player.to_binary_with_game_info(game, yourturn)
        self.write_message(binary_data, binary=True)

        print(f"Client connected. Player ID: {player.player_id}, Game ID: {game.game_id}, and the hand {player.hand} (sent to client)")
    
    def hande_reconnection(self, message):
        _, player_id = struct.unpack("BB", message)
        self.connections[player_id] = self
    
    def handle_draw_card_request(self,message):
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
    
    def handle_move_request(self, message):
        player_id, game_id, color, value = struct.unpack("BBBB", message)
        CreateMove(self.players, self.games, player_id, game_id, color, value, self.connections)
        
        print(f"Player {player_id} did action , card: {color}-{value}, hand size: ")

        

if __name__ == "__main__":
    app = tornado.web.Application([
        ("/ws", EchoHandler),
    ])
    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()