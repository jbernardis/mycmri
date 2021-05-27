import threading
import socket
import select
import logging

class SktServer (threading.Thread):
	def __init__(self, ip, port):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.isRunning = False
		self.endOfLife = False
		self.socketLock = threading.Lock()
		self.sockets = []
		self.newSockets = []
		logging.info("Starting socket server at address: %s:%d" % (ip, port))

	def getSockets(self):
		return [x for x in self.sockets]

	def kill(self):
		self.isRunning = False
		self.join()

	def isKilled(self):
		return self.endOfLife

	def sendToAll(self, msg):
		with self.socketLock:
			tl = [x for x in self.sockets]
		for skt, addr in tl:
			self.sendToOne(skt, addr, msg)
			
	def sendToOne(self, skt, addr, msg):
			try:
				nbytes = len(msg).to_bytes(2, "little")
				skt.send(nbytes)
				skt.send(msg)
			except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
				self.deleteSocket(addr)

	def deleteSocket(self, addr):
		with self.socketLock:
			for i in range(len(self.sockets)):
				if self.sockets[i][1] == addr:
					del(self.sockets[i])
					logging.info("Disconnecting socket client at %s" % str(addr))
					return
				
	def getNewSockets(self):
		if len(self.newSockets) == 0:
			return None
		
		with self.socketLock:
			ns = [x for x in self.newSockets]
			self.newSockets = []
			return ns

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
				logging.info("Subscription from address %s" % str(addr))
				with self.socketLock:
					self.sockets.append((skt, addr))
					self.newSockets.append((skt, addr))
				# TODO - notify main thread of new socket so it can send initial reports

		for skt in self.sockets:
			skt[0].close()

		self.endOfLife = True
