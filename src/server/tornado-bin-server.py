import tornado.web
import tornado.websocket
import tornado.ioloop
import struct

# Assuming ManageGame is a function in the GameManage module
from GameManage import ManageGame


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
            youturn = 0
            if len(self.players) % 2 == 0:
                print("First player initialization")
            else:
                youturn = 1
                print("Second player initialization")

            game, player = ManageGame(self.players, self.games)
        
            binary_data = player.to_binary_with_game_info(game,youturn)
            self.write_message(binary_data, binary=True)
            
            print(f"Client connected. Player ID: {player.player_id}, Game ID: {game.game_id}, and the hand {player.hand} (sent to client)")
        if len(message) == 5:
            
            player_id, action, color, value, hand_size = struct.unpack("BBBBB", message)
            print(f"Player {player_id} did action {action}, card: {color}-{value}, hand size: {hand_size}")
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