import threading
import socket
import select

class SktServer (threading.Thread):
	def __init__(self, ip, port):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.isRunning = False
		self.endOfLife = False
		self.socketLock = threading.Lock()
		self.sockets = []
		print("Starting socket server at address: %s:%d" % (ip, port))

	def getSockets(self):
		return [x for x in self.sockets]

	def kill(self):
		self.isRunning = False
		self.join()

	def isKilled(self):
		return self.endOfLife

	def sendToAll(self, msg):
		nbytes = "%04d" % len(msg)
		print(nbytes)
		with self.socketLock:
			tl = [x for x in self.sockets]
		for skt, addr in tl:
			try:
				skt.send(nbytes.encode())
				skt.send(msg)
			except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
				self.deleteSocket(addr)

	def deleteSocket(self, addr):
		with self.socketLock:
			for i in range(len(self.sockets)):
				if self.sockets[i][1] == addr:
					del(self.sockets[i])
					return

	def run(self):
		self.isRunning = True
		addr = (self.ip, self.port)
		s = socket.create_server(addr)
		s.listen()
		slist = [s]

		while self.isRunning:
			readable, _, _ = select.select(slist, [], [], 1)
			if s in readable:
				skt, addr = s.accept()
				with self.socketLock:
					self.sockets.append((skt, addr))

		for skt in self.sockets:
			skt[0].close()

		self.endOfLife = True
