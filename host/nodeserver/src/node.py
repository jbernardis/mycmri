class Node:
	def __init__(self, a, n, i, o, s):
		self.addr = a
		self.name = n
		self.ninputs = i
		self.noutputs = o
		self.nservos = s
		
		self.inputs = [True for _ in range(i*8)]		
		self.outputs = [False for _ in range(o*8)]
		self.servos = [[0 for _ in range(4)] for _ in range(s*16)]
		
	def getName(self):
		return self.name
		
	def getNInputs(self):
		return self.ninputs*8
	
	def setNInputs(self, i):
		self.ninputs = i
		self.inputs = [True for _ in range(i*8)]
		
	def setInput(self, ix, val):
		self.inputs[ix] = val
		
	def getInputs(self):
		return self.inputs		
		
	def getNOutputs(self):
		return self.noutputs*8
	
	def setNOutputs(self, o):
		self.noutputs = o
		self.outputs = [False for _ in range(o*8)]
		
	def setOutputOn(self, ox):
		self.outputs[ox] = True
		
	def setOutputOff(self, ox):
		self.outputs[ox] = False
		
	def setOutput(self, ox, v):
		self.outputs[ox] = v
		
	def getOutputs(self):
		return self.outputs
		
	def getNServos(self):
		return self.nservos*16
	
	def setNServos(self, s):
		self.nservos = s
		self.servos = [[0 for _ in range(4)] for _ in range(s*16)]
		
	def getServos(self):
		return self.servos
		
	def getTurnoutLimits(self, tx):
		return self.servos[tx][0], self.servos[tx][1], self.servos[tx][2]
		
	def getTurnoutCurrent(self, tx):
		return self.servos[tx][3]
		
	def setTurnoutNormal(self, tx):
		self.servos[tx][3] = self.servos[tx][0]

	def getTurnoutNormal(self, tx):
		return self.servos[tx][0]

	def setTurnoutReverse(self, tx):
		self.servos[tx][3] = self.servos[tx][1]

	def getTurnoutReverse(self, tx):
		return self.servos[tx][1]
		
	def setTurnoutLimits(self, tx, norm, rev, ini):
		self.servos[tx][0] = norm
		self.servos[tx][1] = rev
		self.servos[tx][2] = ini

	def setServoValues(self, sx, norm, rev, ini, cur):
		self.servos[sx][0] = norm
		self.servos[sx][1] = rev
		self.servos[sx][2] = ini
		self.servos[sx][3] = cur
		
	def setServoAngle(self, sx, a):
		self.servos[sx][3] = a
		
	def isNormal(self, sx):
		return self.servos[sx][3] == self.servos[sx][0]
		
	def isReversed(self, sx):
		return self.servos[sx][3] == self.servos[sx][1]

	def __str__(self):
		return("{\"name\": \"%s\", \"address\": %d, \"inputs\": %d,  \"outputs\": %d,  \"servos\": %d}" % (self.name, self.addr, self.ninputs*8, self.noutputs*8, self.nservos*16))


