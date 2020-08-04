
import queue
import serial
import time

from nodesendthreadb import NodeSendThread
from nodeexceptions import NodeException

from nodetypes import OUTPUT_ON, OUTPUT_OFF, INPUT_DELTA, INPUT_CURRENT, TURNOUT_NORMAL, \
		TURNOUT_REVERSE, IDENTIFY, SERVO_ANGLE, SET_TURNOUT, GET_TURNOUT, STORE

class Node:
	def __init__(self):
		self.addr = None
		self.inputs = None
		self.outputs = None
		self.servos = None
		
		self.callbackInput = None
		self.callbackIdentity = None
		self.callbackGetTurnout = None
		self.callbackStore = None
		self.callbackDefault = None
		self.tty = None
		self.baud = None
		self.port = None
		self.cmdQ = queue.Queue(0)
		self.resultQ = queue.Queue(0)
		self.sender = None
		self.receiver = None
		
	def configure(self, naddr, ninputs, noutputs, nservos):
		self.addr = naddr
		self.inputs = ninputs
		self.outputs = noutputs
		self.servos = nservos
		self.sender.registerAddr(self.addr)
		
	def registerCallback(self, cbInput, cbIdentity, cbGetTurnout, cbStore, cbDefault):
		self.callbackInput = cbInput
		self.callbackIdentity = cbIdentity
		self.callbackGetTurnout = cbGetTurnout
		self.callbackStore = cbStore
		self.callbackDefault = cbDefault		

	def connect(self, tty, baud):
		self.tty = tty
		self.baud = baud
		try:
			self.port = serial.Serial(port=self.tty, baudrate=self.baud, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_TWO, timeout=0.5)

		except serial.SerialException:
			self.port = None
			raise NodeException("Unable to Connect")

		time.sleep(2)

	def start(self, poll=True):
		self.sender = NodeSendThread(self, self.addr, self.port, self.cmdQ, self.resultQ, INPUT_DELTA)
		self.sender.start()
		self.setPoll(poll)

	def stop(self):
		self.sender.kill()
		self.sender.join()
		self.sender = None

	def disconnect(self):
		self.port.close()
		self.port = None
		
	def setPoll(self, flag=True):
		if self.sender is None:
			return
		
		self.sender.setPoll(flag)
		
	def process(self):
		while not self.resultQ.empty():
			try:
				cmd, res = self.resultQ.get(False)
			except queue.Empty:
				cmd = None
				
			if cmd is None:
				break
			
			if cmd == INPUT_DELTA:
				if not self.callbackInput is None:
					rv = [[res[i], res[i+1]] for i in range(0, len(res), 2)]
					if len(rv) != 0:
						self.callbackInput(self.addr, rv, True)

			elif cmd == INPUT_CURRENT:
				if not self.callbackInput is None:
					rv = [[i, res[i]] for i in range(len(res))]
					self.callbackInput(self.addr, rv, False)
						
			elif cmd == IDENTIFY:
				if not self.callbackIdentity is None:
					self.callbackIdentity(res[0], res[1], res[2], res[3])
						
			elif cmd == GET_TURNOUT:
				if not self.callbackGetTurnout is None:
					self.callbackGetTurnout(self.addr, res[0], res[1], res[2], res[3])

			elif cmd == STORE:
				if not self.callbackStore is None:
					self.callbackStore(self.addr, res)

			else:
				if not self.callbackDefault is None:
					self.callbackDefault(self.addr, cmd, res)
			
	def getIdentity(self):
		self.cmdQ.put(IDENTIFY)
			
	def getCurrentInput(self):
		self.cmdQ.put(INPUT_CURRENT)
			
	def getDeltaInput(self):
		self.cmdQ.put(INPUT_DELTA)

	def setAngle(self, tx, a):
		cmd = SERVO_ANGLE + bytes([tx & 0xff, a & 0xff])
		self.cmdQ.put(cmd)
		
	def getTurnoutLimits(self, tx):
		cmd = GET_TURNOUT + bytes([tx & 0xff])
		self.cmdQ.put(cmd)
		
	def setTurnoutLimits(self, tx, norm, rev, ini=None):
		if ini is None:
			ival = norm
		else:
			ival = ini
			
		cmd = SET_TURNOUT + bytes([tx & 0xff, norm & 0xff, rev & 0xff, ival & 0xff])
		self.cmdQ.put(cmd)
		
	def store(self):
		self.cmdQ.put(STORE)

	def setTurnoutReverse(self, tx):
		cmd = TURNOUT_REVERSE + bytes([tx & 0xff])
		self.cmdQ.put(cmd)

	def setTurnoutNormal(self, tx):
		cmd = TURNOUT_NORMAL + bytes([tx & 0xff])
		self.cmdQ.put(cmd)

	def setOutputOn(self, ox):
		cmd = OUTPUT_ON + bytes([ox & 0xff])
		self.cmdQ.put(cmd)

	def setOutputOff(self, ox):
		cmd = OUTPUT_OFF + bytes([ox & 0xff])
		self.cmdQ.put(cmd)
