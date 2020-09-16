import json

class TriggerTable:
	def __init__(self, towers):
		self.towers = towers
		self.nBytes = {}
		self.inputsMap = {}
		for t in towers:
			self.nBytes[t[0]] = t[1]
			self.inputsMap[t[0]] = [0xff]*t[1]
			
		self.rules = []
		self.ruleIndex = {}
		
		with open("rules.json", "r") as fp:
			rules = json.load(fp)

		print(json.dumps(rules, sort_keys=True, indent=4))
		
		rct = 0
		for r in rules:
			if len(r) != 2:
				print("Invalid rule in position %d.  Ignoring" % rct)
			else:
				self.addRule(r[0], r[1])
			rct += 1

	def updateInput(self, addr, ix, ival):
		byteIndex, bitIndex = self.getIndices(ix)
		mask = 1 << bitIndex

		if ival:
			self.inputsMap[addr][byteIndex] |= mask
		else:
			self.inputsMap[addr][byteIndex] ^= mask
		
	def updateInputs(self, addr, imap):
		for i in range(len(imap)):
			self.updateInput(addr, i, imap[i])
		
	def checkInputTrigger(self, addr, ix):
		if addr not in self.ruleIndex:
			return []
		if addr not in self.inputsMap:
			return []
		if ix not in self.ruleIndex[addr]:
			return []
		
		actions = []
		
		for r in self.ruleIndex[addr][ix]:
			checkFailed = False			
			# True rules
			tr = self.rules[r][0]
			for addr, rl in tr.items():
				for i in range(len(rl)):
					v = self.inputsMap[addr][i] & rl[i]
					if v != rl[i]:
						checkFailed = True
						break
			if checkFailed:
				continue
				
			# False rules
			tr = self.rules[r][1]
			for addr, rl in tr.items():
				for i in range(len(rl)):
					v = ~self.inputsMap[addr][i] & rl[i]
					if v != rl[i]:
						checkFailed = True
						break
			if checkFailed:
				continue

			actions.extend(self.rules[r][2])
		
		return actions
	
	def addRule(self, conditions, actions):
		self.actions = actions
		trueCond = {}
		falseCond = {}
		
		rx = len(self.rules)
		for addr, inp, val in conditions:
			if addr not in self.nBytes:
				print("Address %d referenced in rule has not been defined - skipping" % addr)
				continue

			byteIndex, bitIndex = self.getIndices(inp)
			mask = 1 << bitIndex
			if addr not in self.ruleIndex:
				self.ruleIndex[addr] = {}
				
			if inp not in self.ruleIndex[addr]:
				self.ruleIndex[addr][inp] = []
				
			self.ruleIndex[addr][inp].append(rx)
	
			if val:
				if addr not in trueCond:
					trueCond[addr] = [0] * self.nBytes[addr]
				trueCond[addr][byteIndex] |= mask
			else:
				if addr not in falseCond:
					falseCond[addr] = [0] * self.nBytes[addr]
				falseCond[addr][byteIndex] |= mask
		self.rules.append([trueCond, falseCond, actions])
			
	def getIndices(self, ix):
		byteIndex = int(ix/8)
		bitIndex = ix % 8
		return byteIndex, bitIndex

