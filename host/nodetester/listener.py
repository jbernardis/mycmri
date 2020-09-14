
import threading
import socket

class Listener(threading.Thread):
	def __init__(self, parent, ip, port):
		threading.Thread.__init__(self)
		self.parent = parent
		self.skt = socket.create_connection((ip, port))
		self.skt.setblocking(True)
		self.isRunning = False
		self.endOfLife = False
		
	def kill(self):
		self.isRunning = False

	def isKilled(self):
		return self.endOfLife
	
	def run(self):
		self.isRunning = True
		while self.isRunning:
			try:
				b = self.skt.recv(1024)
				if len(b) == 0:
					self.parent.raiseMessageEvent("socket closed")
					break

				self.parent.raiseInputsEvent(b)

			except socket.timeout:
				self.parent.raiseMessageEvent("timeout exception")
		
		self.endOfLife = True

