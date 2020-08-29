
import queue
import serial
import time

from nodesendthreadb import NodeSendThread
from nodeexceptions import NodeException

from nodetypes import OUTPUT_ON, OUTPUT_OFF, OUTPUT_CURRENT, INPUT_DELTA, INPUT_CURRENT, TURNOUT_NORMAL, \
		TURNOUT_REVERSE, IDENTIFY, SERVO_ANGLE, SET_TURNOUT, GET_TURNOUT, STORE

class Bus:
	def __init__(self):
		self.callbackInput = None
		self.callbackOutput = None
		self.callbackTurnout = None
		self.callbackIdentity = None
		self.callbackStore = None
		self.callbackDefault = None
		self.tty = None
		self.baud = None
		self.port = None
		self.cmdQ = queue.Queue(0)
		self.resultQ = queue.Queue(0)
		self.sender = None
		self.receiver = None
		
	def registerInputCallback(self, cbInput):
		self.callbackInput = cbInput
		
	def registerOutputCallback(self, cbOutput):
		self.callbackOutput = cbOutput

	def registerTurnoutCallback(self, cbTurnout):
		self.callbackTurnout = cbTurnout
		
	def registerIdentityCallback(self, cbIdentity):
		self.callbackIdentity = cbIdentity

	def registerDefaultCallback(self, cbDefault):
		self.callbackDefault = cbDefault		

	def connect(self, tty, baud):
		self.tty = tty
		self.baud = baud
		try:
			self.port = serial.Serial(port=self.tty, baudrate=self.baud, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO, timeout=5)

		except serial.SerialException:
			self.port = None
			raise NodeException("Unable to Connect to serial port %s" % tty)

		time.sleep(2)

	def start(self, addrList):
		self.addrList = addrList
		self.sender = NodeSendThread(self, self.port, self.cmdQ, self.resultQ, INPUT_DELTA)
		self.sender.start()
		for a in self.addrList:
			self.setPoll(a, False)  #TODO for all known addrs

	def stop(self):
		self.sender.kill()
		self.sender.join()
		self.sender = None

	def disconnect(self):
		self.port.close()
		self.port = None
		
	def setPoll(self, addr, flag=True):
		if self.sender is None:
			return
		
		self.sender.setPoll(addr, flag)
		
	def process(self):
		while not self.resultQ.empty():
			try:
				addr, cmd, res = self.resultQ.get(False)
			except queue.Empty:
				cmd = None
				
			if cmd is None:
				break
			
			if cmd == INPUT_DELTA:
				if not self.callbackInput is None:
					rv = [[res[i], res[i+1]] for i in range(0, len(res), 2)]
					self.callbackInput(addr, rv, True)

			elif cmd == INPUT_CURRENT:
				if not self.callbackInput is None:
					rv = [[i, res[i]] for i in range(len(res))]
					self.callbackInput(addr, rv, False)

			elif cmd == OUTPUT_CURRENT:
				if not self.callbackOutput is None:
					self.callbackOutput(addr, res)
						
			elif cmd == IDENTIFY:
				if not self.callbackIdentity is None:
					self.callbackIdentity(res[0], res[1], res[2], res[3])
						
			elif cmd == GET_TURNOUT:
				if not self.callbackTurnout is None:					
					rv = [[res[i], res[i+1], res[i+2], res[i+3]] for i in range(0, len(res), 4)]
					self.callbackTurnout(addr, rv)

			else:
				if not self.callbackDefault is None:
					self.callbackDefault(addr, cmd, res)
			
	def getIdentity(self, addr):
		self.cmdQ.put((addr, IDENTIFY))
			
	def getCurrentInput(self, addr):
		self.cmdQ.put((addr, INPUT_CURRENT))
			
	def getCurrentOutput(self, addr):
		self.cmdQ.put((addr, OUTPUT_CURRENT))
			
	def getDeltaInput(self, addr):
		self.cmdQ.put((addr, INPUT_DELTA))

	def setAngle(self, addr, tx, a):
		cmd = SERVO_ANGLE + bytes([tx & 0xff, a & 0xff])
		self.cmdQ.put((addr, cmd))
		
	def getTurnouts(self, addr):
		self.cmdQ.put((addr, GET_TURNOUT))
		
	def setTurnoutLimits(self, addr, tx, norm, rev, ini=None):
		if ini is None:
			ival = norm
		else:
			ival = ini
			
		cmd = SET_TURNOUT + bytes([tx & 0xff, norm & 0xff, rev & 0xff, ival & 0xff])
		self.cmdQ.put((addr, cmd))
		
	def store(self, addr):
		self.cmdQ.put((addr, STORE))

	def setTurnoutReverse(self, addr, tx):
		cmd = TURNOUT_REVERSE + bytes([tx & 0xff])
		self.cmdQ.put((addr, cmd))

	def setTurnoutNormal(self, addr, tx):
		cmd = TURNOUT_NORMAL + bytes([tx & 0xff])
		self.cmdQ.put((addr, cmd))

	def setOutputOn(self, addr, ox):
		cmd = OUTPUT_ON + bytes([ox & 0xff])
		self.cmdQ.put((addr, cmd))

	def setOutputOff(self, addr, ox):
		cmd = OUTPUT_OFF + bytes([ox & 0xff])
		self.cmdQ.put((addr, cmd))
