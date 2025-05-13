import tornado.web
import tornado.websocket
import tornado.ioloop
import struct
import math


class EchoHandler(tornado.websocket.WebSocketHandler):

	def open(self):
		print("open")

	def on_close(self):
		print("close")

	def on_message(self, message):
		val = struct.unpack(">hh", message)
		print("[{},{}]".format(val[0],val[1]))
		len = math.sqrt(val[0]*val[0]+val[1]*val[1])
		data = struct.pack(">iif", val[0], val[1], len)
		self.write_message(data, binary=True)

	def check_origin(self, origin):
		return True


if __name__ == "__main__":
	app = tornado.web.Application([
		("/ws", EchoHandler),
	])
	app.listen(8000)
	tornado.ioloop.IOLoop.instance().start()