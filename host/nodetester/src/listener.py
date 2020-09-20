
import threading
import socket

class Listener(threading.Thread):
	def __init__(self, parent, ip, port):
		threading.Thread.__init__(self)
		self.parent = parent
		self.skt = socket.create_connection((ip, port))
		self.skt.settimeout(0.5)
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
				b = self.skt.recv(4)
				if len(b) == 0:
					self.skt.close()
					self.parent.raiseDisconnectEvent()
					self.isRunning = False
				elif len(b) == 4:
					ct = int(b)
					b = self.skt.recv(ct)
					if len(b) != ct:
						print("did not receive expected number of bytes: expected %d received %d" % (ct, len(b)))
					else:
						self.parent.raiseDeliveryEvent(b)
				else:
					print("did not receive expected number of bytes: expected %d received %d" % (4, len(b)))

			except socket.timeout:
				pass
		
		self.endOfLife = True

