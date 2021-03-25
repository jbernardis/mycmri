import evaluate

		
class TriggerTable:
	def __init__(self, nodes):
		self.nodes = nodes
		self.inputsMap = {}
		self.flagsMap = {}
		self.registersMap = {}
		for t in nodes:
			self.inputsMap[t[0]] = [True for _ in range(t[1] * 8)]
			self.outputsMap[t[0]] = [True for _ in range(t[2] * 8)]
			self.flagsMap[t[0]] = [False for _ in range(t[3])]
			self.registersMap[t[0]] = ["" for _ in range(t[4])]
			
		evaluate.initialize(self.inputsMap, self.outputsMap, self.flagsMap, self.registersMap)
			
		
	def updateInputs(self, addr, imap):
		for i in range(len(imap)):
			self.inputsMap[addr][i] = imap[i]
			
	def updateInput(self, addr, ix, val):
		self.inputsMap[addr][ix] = val
		
	def updateOutputs(self, addr, omap):
		for i in range(len(omap)):
			self.outputsMap[addr][i] = omap[i]
			
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