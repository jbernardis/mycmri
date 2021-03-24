import evaluate

		
class TriggerTable:
	def __init__(self, nodes):
		self.nodes = nodes
		self.nBytes = {}
		self.nFlags = {}
		self.nRegisters = {}
		self.inputsMap = {}
		self.flagsMap = {}
		self.registersMap = {}
		for t in nodes:
			self.nBytes[t[0]] = t[1]
			self.inputsMap[t[0]] = [True for _ in range(t[1] * 8)]
			self.nFlags[t[0]] = t[2]
			self.flagsMap[t[0]] = [False for _ in range(t[2])]
			self.nRegisters[t[0]] = t[3]
			self.registersMap[t[0]] = ["" for _ in range(t[3])]
			
		evaluate.initialize(self.inputsMap, self.flagsMap, self.registersMap)
			
		
	def updateInputs(self, addr, imap):
		for i in range(len(imap)):
			self.inputsMap[addr][i] = imap[i]
			
	def updateInput(self, addr, ix, val):
		self.inputsMap[addr][ix] = val
		
	def updateFlags(self, addr, flags):
		for i in range(len(flags)):
			self.flagsMap[addr][i] = flags[i]
		
	def updateRegisterss(self, addr, regs):
		for i in range(len(regs)):
			self.registersMap[addr][i] = regs[i]
		
	def checkTriggers(self, addr):
		if addr not in self.inputsMap:
			return []	
		
		return evaluate.evaluate()