import json
import logging

CTYPE_INPUT = 'i'
CTYPE_FLAG = 'f'
CTYPE_REGISTER = 'r'

class Condition:
	def __init__(self, ctype, addr, idx, val):
		self.ctype = ctype
		self.addr = addr
		self.idx = idx
		self.val = val

	def getType(self):
		return self.ctype
			
	def getAddr(self):
		return self.addr
			
	def getIndex(self):
		return self.idx
	
	def getValue(self):
		return self.val
		
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
			self.inputsMap[t[0]] = [True] * (t[1] * 8)
			self.nFlags[t[0]] = t[2]
			self.flagsMap[t[0]] = [False] * t[2]
			self.nRegisters[t[0]] = t[3]
			self.registersMap[t[0]] = [""] * t[3]
			
		self.rules = []
		
		with open("rules.json", "r") as fp:
			rules = json.load(fp)
			
		logging.info("rules loaded: " + json.dumps(rules, sort_keys=True, indent=4))
		
		rct = 0
		for r in rules["rules"]:
			if len(r) != 2:
				logging.warning("Invalid rule in position %d.  Ignoring" % rct)
			else:
				self.addRule(r["conditions"], r["actions"])
			rct += 1
		
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
	
	def addRule(self, conditions, actions):
		self.actions = actions
		rconditions = []
		
		for c in conditions:
			try:
				ctype, addr, idx, val = c
			except ValueError:
				logging.warning("Unable to parse condition: %s - skipping" % str(c))
				continue
			
			if addr not in self.nBytes:
				logging.warning("Address %d referenced in rule has not been defined - skipping" % addr)
				continue
			rconditions.append(Condition(ctype, addr, idx, val))

		self.rules.append([rconditions, actions])
		
	def checkTriggers(self, addr):
		if addr not in self.inputsMap:
			return []
		
		triggered = [False] * len(self.rules)
		
		for rx in range(len(self.rules)):
			conditionTriggered = True			
			conditions = self.rules[rx][0]
			logging.info("checking rule %d" % rx)
			for c in conditions:
				ctype = c.getType()
				cvx = c.getIndex()
				caddr = c.getAddr()
				cv = c.getValue()
				if ctype == CTYPE_INPUT:
					v = self.inputsMap[caddr][cvx]
					if not cv == v:
						logging.info("Address %d rule %d rejected for input %d:%d: %s != %s" % (
							addr, rx, caddr, cvx, str(v), str(cv)))
						conditionTriggered = False
						break
					else:
						logging.info("Address %d input %d:%d matched %s" % (addr, caddr, cvx, v))

				elif ctype == CTYPE_FLAG:
					v = self.flagsMap[caddr][cvx]
					if not cv == v:
						logging.info("Address %d rule %d rejected for flag %d:%d: %s != %s" % (
							addr, rx, caddr, cvx, str(v), str(cv)))
						conditionTriggered = False
						break
					else:
						logging.info("Address %d flag %d:%d matched %s" % (addr, caddr, cvx, v))

				elif ctype == CTYPE_REGISTER:
					v = self.registersMap[caddr][cvx]
					if not cv == v:
						logging.info("Address %d rule %d rejected for register %d:%d: %s != %s" % (
							addr, rx, caddr, cvx, str(v), str(cv)))
						conditionTriggered = False
						break
					else:
						logging.info("Address %d register %d:%d matched %s" % (addr, caddr, cvx, v))
						
				else:
					logging.warning("Unknown condition type: %s - skipping" % ctype)
					
			if conditionTriggered:
				logging.info("Condition matched for rule %d" % rx)
				triggered[rx] = True


		actions = []
		for r in range(len(triggered)):
			if triggered[r]:
				actions.extend(self.rules[r][1])
		
		return actions

