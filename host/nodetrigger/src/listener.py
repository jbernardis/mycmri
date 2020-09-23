
import threading
import socket
import json

class Listener(threading.Thread):
	def __init__(self, parent, ip, port, queue):
		threading.Thread.__init__(self)
		self.parent = parent
		self.skt = socket.create_connection((ip, port))
		self.skt.settimeout(0.5)
		self.msgQ = queue
		self.isRunning = False
		self.endOfLife = False
		
	def kill(self):
		self.isRunning = False

	def isKilled(self):
		return self.endOfLife

	def run(self):
		self.isRunning = True
		while self.isRunning:
			totalRead = 0
			szBuf = b''
					
			while totalRead < 4 and self.isRunning:
				try:
					b = self.skt.recv(4-totalRead)
					if len(b) == 0:
						self.skt.close()
						self.sendDisconnect()
						self.isRunning = False
					
				except socket.timeout:
					pass
				else:
					szBuf += b
					totalRead += len(b)
		
		
			if not self.isRunning:
				break
			
			try:
				msgSize = int(szBuf)
			except:
				print("Unable to determine message length: (", szBuf, ")")
				msgSize = None

			if msgSize:		
				totalRead = 0
				msgBuf = b''
		
				while totalRead < msgSize and self.isRunning:		
					try:
						b = self.skt.recv(msgSize - totalRead)
						if len(b) == 0:
							self.skt.close()
							self.sendDisconnect()
							self.isRunning = False
							
					except socket.timeout:
						pass
					else:
						msgBuf += b
						totalRead += len(b)
			
				if self.isRunning:
					if totalRead != msgSize:
						print("did not receive expected number of bytes: expected %d received %d" % (msgSize, totalRead))
					else:
						self.msgQ.put(msgBuf)
	
		self.endOfLife = True
		
	def sendDisconnect(self):
		s = json.dumps({"type": "disconnect"})
		self.msgQ.put(s.encode())
		
