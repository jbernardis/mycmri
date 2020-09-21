import threading
import queue
import time

from nodeexceptions import BusNotConnected, BusReadException, BusTimeoutException
from nodetypes import commandName, ACKNOWLEDGE, ERRORRESPONSE

STX  = b'\x02'  # start byte
ETX  = b'\x03'  # end byte
ESC  = b'\x10'  # escape byte

TX = 1
RX = 2

class NodeSendThread (threading.Thread):
	def __init__(self, node, port, cmdQ, resultQ, pollcmd, pollInterval=0.25):
		threading.Thread.__init__(self)
		self.node = node
		self.port = port
		self.cmdQ = cmdQ
		self.resultQ = resultQ
		self.pollcmd = pollcmd
		self.pollInterval = pollInterval * 1000000000 # convert s to ns
		self.isRunning = False
		self.endOfLife = False
		self.polling = {}
		self.mode = None
		self.setMode(TX)
		
	def setPoll(self, addr, flag):
		self.polling[addr] = flag
	
	def kill(self):
		self.isRunning = False

	def isKilled(self):
		return self.endOfLife
	
	def setMode(self, txrx):
		if self.mode == txrx:
			return 
		
		self.mode = txrx
		
		flag = True if txrx == RX else False
		self.port.dtr = flag
		self.port.rts = flag
		
	def send(self, addr, omsg):
		if self.port is None or not self.port.is_open:
			raise BusNotConnected

		ob = [0] * len(omsg)
		i = 0
		for byte in omsg:
			ob[i] = byte
			i += 1

		self.setMode(TX)
		self.port.write(b'\xFF')
		self.port.write(b'\xFF')
		self.port.write(STX)
		self.port.write(bytes([65 + addr]))
		for byte in ob:
			b = bytes([byte & 0xff])
			if b == ETX:
				self.port.write(ESC) # escape because this looks like an STX bit (very basic protocol)
			elif b == ESC:
				self.port.write(ESC) # escape because this looks like an escape bit (very basic protocol)
			self.port.write(b)

		self.port.write(ETX)
		self.port.flush()
		
	def recv(self):
		InBuffer = []
		self.setMode(RX)
		c = b'\xFF'
		while c == b'\xFF':
			c = self.port.read()
			if len(c) == 0:
				raise BusTimeoutException

		if c != STX:
			raise BusReadException

		paddr = self.port.read()
		if len(paddr) == 0:
			raise BusTimeoutException

		addr = ord(paddr) - 65
		
		cmd = self.port.read()
		if len(cmd) == 0:
			raise BusTimeoutException

		c = self.port.read()
		if len(c) == 0:
			raise BusTimeoutException
		
		while c != ETX:
			if c == ESC or c == ETX:
				c = self.port.read()

			InBuffer.append(ord(c))
			c = self.port.read()
			if len(c) == 0:
				raise BusTimeoutException
		
		self.setMode(TX)
		return addr, cmd, InBuffer

		
	def run(self):
		self.isRunning = True
		lastPoll = time.monotonic_ns()
		while self.isRunning:
			if self.port is None or not self.port.is_open:
				raise BusNotConnected

			# see if it's time to poll and add commands to the queue if so						
			current = time.monotonic_ns()
			elapsed = current - lastPoll
			if self.isRunning and elapsed > self.pollInterval:
				for a in self.polling:
					if self.polling[a]:
						self.cmdQ.put((a, self.pollcmd))
				lastPoll = current

			try:
				addr, cmd = self.cmdQ.get(False)
			except queue.Empty:
				cmd = None
					
			if self.isRunning:
				if not cmd is None:
					# every command needs a response.  Since this is a half-duplex master/slave bus, we must wait
					# for the response before we can proceed with the next command
					scmd = bytes([cmd[0]])
					self.send(addr, cmd)
					noResult = True
					while noResult:					
						buffer = ""
						try:
							naddr, ncmd, buffer = self.recv()
						except BusTimeoutException:
							msg = "Node at address %d has timed out responding to command %s" % (addr, commandName(scmd))
							self.resultQ.put((addr, ERRORRESPONSE, msg))
							noResult = False
						
						except BusReadException:
							msg = "Invalid response from address %d for command %s" % (addr, commandName(scmd))
							self.resultQ.put((addr, ERRORRESPONSE, msg))
							noResult = False
						
						else:
							if naddr != addr:
								# message from a different node?? - throw it away and keep waiting
								msg = "Mis-addressed message: expected address %d, received %d" % (addr, naddr)
								self.resultQ.put((addr, ERRORRESPONSE, msg))
			
							elif ncmd != scmd and ncmd != ACKNOWLEDGE:
								# message from different command?? - throw it away and keep waiting
								msg = "Unexpected command type from address %d - expecting %s, got %s" % (naddr, commandName(scmd), commandName(ncmd))
								self.resultQ.put((addr, ERRORRESPONSE, msg))
	
							else:
								# this is the expected result - but we eat acknowledgements
								if ncmd != ACKNOWLEDGE:
									# only report a good response if it's not an ack
									self.resultQ.put((naddr, ncmd, buffer))
								noResult = False
		
				
		self.endOfLife = True
