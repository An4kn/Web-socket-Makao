import tornado.web
import tornado.websocket
import tornado.ioloop
import struct

# Assuming ManageGame is a function in the GameManage module
from GameManage import FirstConnection, CreateMove


class EchoHandler(tornado.websocket.WebSocketHandler):

    games = {}
    players = {}

    def open(self):
        # print("open") #moze nawet wopen w sumie
        # game, player = ManageGame(self.players, self.games)
        
        # binary_data = player.to_binary_with_game_info(game.game_id)
        # self.write_message(binary_data, binary=True)
        
        # print(f"Client connected. Player ID: {player.player_id}, Game ID: {game.game_id}, and the hand {player.hand} (sent to client)")
        pass
    def on_close(self):
        print("close")

    # def on_message(self, message):
    # 	val = struct.unpack(">hh", message)
    # 	print("[{},{}]".format(val[0],val[1]))
    # 	len = math.sqrt(val[0]*val[0]+val[1]*val[1])
    # 	data = struct.pack(">iif", val[0], val[1], len)
    # 	self.write_message(data, binary=True)

    def on_message(self, message):
        # if len(message) != 6:
        #     print(f"Invalid message length: {len(message)} bytes")
        #     return
        print(f"Received message: {message}")
        if len(message) == 1: #initialization'
            
            # first_player_initialization = struct.unpack("B", message)
            yourturn = 0
            if len(self.players) % 2 == 0:
                print("First player initialization")
            else:
                yourturn = 1
                print("Second player initialization")

            game, player = FirstConnection(self.players, self.games)
        
            binary_data = player.to_binary_with_game_info(game,yourturn)
            self.write_message(binary_data, binary=True)
            
            print(f"Client connected. Player ID: {player.player_id}, Game ID: {game.game_id}, and the hand {player.hand} (sent to client)")
        
        if len(message) == 2:
            # player_click = struct.unpack("BB", message)
            # print(f"Player clicked: {player_click}")
            player_id, game_id = struct.unpack("BB", message)
            # print(f"Player ID: {player_id}, Game ID: {game_id}")
            # ManageGame(self.players, self.games, player_id, game_id)
        if len(message) == 4:
            
            player_id, game_id, color, value = struct.unpack("BBBB", message)
            CreateMove(self.players, self.games, player_id, game_id, color, value)
            
            print(f"Player {player_id} did action , card: {color}-{value}, hand size: ")

        # ManageGame(self.players, self.games)
    # id sesji
    # inicjalizacja
    
    def check_origin(self, origin):
        return True

if __name__ == "__main__":
    app = tornado.web.Application([
        ("/ws", EchoHandler),
    ])
    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()