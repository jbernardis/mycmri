#!/usr/bin/env python3

class Output:
	def __init__(self):
		self.value = False
		
	def setValue(self, nv):
		self.value = nv
		
	def getValue(self):
		print("output level, returning %s" % self.value)
		return self.value
		
class Input:
	def __init__(self):
		self.value = True
		
	def setValue(self, nv):
		self.value = nv
		
	def getValue(self):
		print("input level, returning %s" % self.value)
		return self.value
	
class Servo:
	def __init__(self):
		self.normal = 0
		self.reverse = 0
		self.initial = 0
		self.current = 0
		
	def setValues(self, n, r, i, c):
		self.normal = n
		self.reverse = r
		self.initial = i
		self.current = c
		
	def getValues(self):
		return self.normal, self.reverse, self.initial, self.current
	
	def setLimits(self, n, r, i):
		self.normal = n
		self.reverse = r
		if i is None:
			self.initial = self.normal
		else:
			self.initial = i
			
	def setCurrent(self, c):
		self.current = c
		
class Node:
	def __init__(self, addr, nm, i, o, s):
		self.addr = addr
		self.name = nm
		
		self.inputs = []
		for _ in range(i):
			self.inputs.append(Input())
		self.ninputs = i
		
		self.outputs = []
		for _ in range(o):
			self.outputs.append(Output())
		self.noutputs = o
		
		self.servos = []
		for _ in range(s):
			self.servos.append(Servo())
		self.nservos = s
		#print("add node %s a:%d i:%d o:%d s:%d" % (nm, addr, i, o, s))
		
	def getAddr(self):
		return self.addr
	
	def getName(self):
		return self.name
	
	def getOutput(self, n):
		if n < 0 or n > self.noutputs:
			print("outputs index of %d is out of range for node %s(%d)" % (n, self.name, self.addr))
			return False
		
		print("node level: %d" % n)		
		return self.outputs[n].getValue()
	
	def setOutputs(self, n, vals):
		if n < 0 or n > self.noutputs:
			print("outputs count of %d is out of range for node %s(%d)" % (n, self.name, self.addr))
			return

		diffs = 0		
		for i in range(n):
			if self.outputs[i].getValue() != vals[i]:
				diffs += 1
				self.outputs[i].setValue(vals[i])
				
		return diffs
			
	def setOutputsDelta(self, n, vals):
		if n < 0 or n > self.noutputs:
			print("outputs count of %d is out of range for node %s(%d)" % (n, self.name, self.addr))
			return
		
		diffs = 0
		for i in range(n):
			if self.outputs[vals[i][0]].getValue() != vals[i][1]:
				diffs += 1
				self.outputs[vals[i][0]].setValue(vals[i][1])
				
		return diffs
			
	def getInput(self, n):
		if n < 0 or n > self.ninputs:
			print("inputs index of %d is out of range for node %s(%d)" % (n, self.name, self.addr))
			return True

		print("node level: %d" % n)		
		return self.inputs[n].getValue()
			
	def setInputs(self, n, vals):
		if n < 0 or n > self.ninputs:
			print("inputs count of %d is out of range for node %s(%d)" % (n, self.name, self.addr))
			return
		
		diffs = 0
		for i in range(n):
			if self.inputs[i].getValue() != vals[i]:
				diffs += 1
				self.inputs[i].setValue(vals[i])
				
		return diffs
			
	def setInputsDelta(self, n, vals):
		if n < 0 or n > self.noutputs:
			print("inputs count of %d is out of range for node %s(%d)" % (n, self.name, self.addr))
			return
		
		diffs = 0
		for i in range(n):
			if self.inputs[vals[i][0]].getValue() != vals[i][1]:
				diffs += 1
				self.inputs[vals[i][0]].setValue(vals[i][1])
				
		return diffs
			
	def setServos(self, n, vals):
		if n < 0 or n > self.nservos:
			print("servos count of %d is out of range for node %s(%d)" % (n, self.name, self.addr))
			return
		
		for i in range(n):
			self.servos[i].setValues(vals[i][0], vals[i][1], vals[i][2], vals[i][3])
			
	def setServosDelta(self, n, vals):
		if n < 0 or n > self.nservos:
			print("servos count of %d is out of range for node %s(%d)" % (n, self.name, self.addr))
			return
		
		for i in range(n):
			self.servos[vals[i][0]].setCurrent(vals[i][1])
			
	def setServosLimits(self, n, vals):
		if n < 0 or n > self.nservos:
			print("servos count of %d is out of range for node %s(%d)" % (n, self.name, self.addr))
			return
		
		for i in range(n):
			self.servos[vals[i][0]].setLimits(vals[i][1], vals[i][2], vals[i][3])
			
