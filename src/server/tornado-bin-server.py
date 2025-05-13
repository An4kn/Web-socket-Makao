import tornado.web
import tornado.websocket
import tornado.ioloop
import struct

# Assuming ManageGame is a function in the GameManage module
from .GameManage import ManageGame


class EchoHandler(tornado.websocket.WebSocketHandler):

    games = {}
    players = {}

    def open(self):
        print("open")

    def on_close(self):
        print("close")

    # def on_message(self, message):
    # 	val = struct.unpack(">hh", message)
    # 	print("[{},{}]".format(val[0],val[1]))
    # 	len = math.sqrt(val[0]*val[0]+val[1]*val[1])
    # 	data = struct.pack(">iif", val[0], val[1], len)
    # 	self.write_message(data, binary=True)

    def on_message(self, message):
        if len(message) != 5:
            print(f"Invalid message length: {len(message)} bytes")
            return
        player_id, action, color, value, hand_size = struct.unpack("BBBBB", message)
        print(f"Player {player_id} did action {action}, card: {color}-{value}, hand size: {hand_size}")
        ManageGame(self.players, self.games)
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