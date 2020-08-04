import threading
import queue
import time

from nodeexceptions import NodeNotConnected, NodeReadException, NodeAddressException
from nodetypes import ACKNOWLEDGE, IDENTIFY

STX  = b'\x02'  # start byte
ETX  = b'\x03'  # end byte
ESC  = b'\x10'  # escape byte

MAXOUTSTANDING = 5

class NodeSendThread (threading.Thread):
	def __init__(self, node, addr, port, cmdQ, resultQ, pollcmd, pollInterval=0.25):
		threading.Thread.__init__(self)
		self.node = node
		self.addr = addr
		self.port = port
		self.cmdQ = cmdQ
		self.resultQ = resultQ
		self.pollcmd = pollcmd
		self.pollInterval = pollInterval * 1000000000 # convert s to ns
		self.isRunning = False
		self.endOfLife = False
		self.polling = False
		
	def registerAddr(self, addr):
		self.addr = addr
		
	def setPoll(self, flag):
		self.polling = flag
	
	def kill(self):
		self.isRunning = False

	def isKilled(self):
		return self.endOfLife
		
	def send(self, omsg):
		if self.port is None or not self.port.is_open:
			raise NodeNotConnected

		ob = [0] * len(omsg)
		i = 0
		for byte in omsg:
			ob[i] = byte
			i += 1

		self.port.write(b'\xFF')
		self.port.write(b'\xFF')
		self.port.write(STX)
		if ob[0] == IDENTIFY:
			self.port.write(bytes[30]) # broadcast addr
		else:
			self.port.write(bytes([65 + self.addr]))
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
		c = b'\xFF'
		while c == b'\xFF':
			c = self.port.read()
			if len(c) == 0:
				raise NodeReadException

		if c != STX:
			raise NodeReadException

		addr = self.port.read()
		if len(addr) == 0:
			raise NodeReadException
		if addr != bytes([65 + self.addr]):  #elf.addr:
			raise NodeAddressException(addr, self.addr)
		
		cmd = self.port.read()
		if len(cmd) == 0:
			raise NodeReadException

		c = self.port.read()
		if len(c) == 0:
			raise NodeReadException
		
		while c != ETX:
			if c == ESC or c == ETX:
				c = self.port.read()

			InBuffer.append(ord(c))
			c = self.port.read()
			if len(c) == 0:
				raise NodeReadException
		
		#if cmd != ACKNOWLEDGE:
			#print("rcv")
			#for c in InBuffer:
				#print("%02x " % c)
			#print("====")
		return cmd, InBuffer

		
	def run(self):
		self.isRunning = True
		lastPoll = time.monotonic_ns()
		self.outstanding = 0
		while self.isRunning:
			if self.port is None or not self.port.is_open:
				raise NodeNotConnected

			if self.port.in_waiting > 0:
				cmd, buffer = self.recv()

				if cmd == ACKNOWLEDGE:
					self.outstanding -= 1
				else:
					self.resultQ.put((cmd, buffer))

				buffer = ""
						
			if self.outstanding < MAXOUTSTANDING and not self.cmdQ.empty():
				try:
					cmd = self.cmdQ.get(True)
				except queue.Empty:
					cmd = None
					
				if self.isRunning:
					if not cmd is None:
						self.send(cmd)
						#print("sending: ")
						#for c in cmd:
							#print("%02x" % c);
						#print("===")
						self.outstanding += 1
					
			if self.outstanding < MAXOUTSTANDING:
				current = time.monotonic_ns()
				elapsed = current - lastPoll
				if self.isRunning and elapsed > self.pollInterval:
					if self.polling:
						self.send(self.pollcmd)
						self.outstanding += 1
					lastPoll = current
				
				
		self.endOfLife = True
