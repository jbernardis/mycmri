#!/usr/bin/env python3

from node import Node
import evaluate

import pprint


class Railroad:
	def __init__(self, server):
		self.server = server
		self.nodes = []
		self.nodeMap = {}
		
	def addNode(self, n):
		self.nodes.append(n)
		self.nodeMap[n.getAddr()] = n
		
	def getInput(self, addr, idx):
		try:
			nd = self.nodeMap[addr]
		except KeyError:
			print("Node Address %d not found" % addr)
			return True
		
		print("rr level %d %d" % (addr, idx))
		
		return nd.getInput(idx)
		
	def getOutput(self, addr, idx):
		try:
			nd = self.nodeMap[addr]
		except KeyError:
			print("Node Address %d not found" % addr)
			return False
		
		
		print("rr level %d %d" % (addr, idx))
		return nd.getOutput(idx)
		
	def updateInputs(self, jo):
		try:
			addr = jo["address"]
		except KeyError:
			print("Node address missing from inputs report")
			return False
		
		try:
			node = self.nodeMap[addr]
			
		except KeyError:
			print("node with address %d unknown" % addr)
			return False
		
		try:
			n = jo["count"]
			
		except KeyError:
			print("count missing from inputs report")
			return False
		
		try:
			il = jo["values"]
			
		except KeyError:
			print("values list missing from inputs report")
			return False
		
		try:
			delta = jo["delta"]
			
		except KeyError:
			delta = False
			
		if delta:
			changes = node.setInputsDelta(n, il)
		else:
			changes = node.setInputs(n, il)
			
		return changes != 0
		
	def updateOutputs(self, jo):
		try:
			addr = jo["address"]
		except KeyError:
			print("Node address missing from outputs report")
			return
		
		try:
			node = self.nodeMap[addr]
			
		except KeyError:
			print("node with address %d unknown" % addr)
			return 
		
		try:
			n = jo["count"]
			
		except KeyError:
			print("count missing from outputs report")
			return 
		
		try:
			ol = jo["values"]
			
		except KeyError:
			print("values list missing from outputs report")
			return 
		
		try:
			delta = jo["delta"]
			
		except KeyError:
			delta = False
			
		if delta:
			node.setOutputsDelta(n, ol)
		else:
			node.setOutputs(n, ol)
		
	def updateServos(self, jo):
		try:
			addr = jo["address"]
		except KeyError:
			print("Node address missing from servos report")
			return
		
		try:
			node = self.nodeMap[addr]
			
		except KeyError:
			print("node with address %d unknown" % addr)
			return 
		
		try:
			n = jo["count"]
			
		except KeyError:
			print("count missing from servos report")
			return 
		
		try:
			ol = jo["values"]
			
		except KeyError:
			print("values list missing from servos report")
			return 
		
		try:
			delta = jo["delta"]
			
		except KeyError:
			delta = False
		
		try:
			limits = jo["limits"]
			
		except KeyError:
			limits = False
			
		if delta:
			if limits:				
				node.setServosLimits(n, ol)
			else:
				node.setServosDelta(n, ol)
		else:
			node.setServos(n, ol)
			
	def processMsg(self, jdata):
		triggerEval = False
		if "nodes" in jdata.keys():
			for nd in jdata["nodes"]:
				self.addNode(Node(nd["address"], nd["name"], nd["input"], nd["output"], nd["servo"]))
				
		elif "outputs" in jdata.keys():
			self.updateOutputs(jdata["outputs"])
			
		elif "inputs" in jdata.keys():
			triggerEval = self.updateInputs(jdata["inputs"])
			
		elif "servos" in jdata.keys():
			self.updateServos(jdata["servos"])
			
		else:
			print("Unexpected message:")
			pprint.pprint(jdata)
			print("==================================")

		if triggerEval:
			actions = evaluate.evaluate()
			if len(actions) > 0:
				self.performActions(actions)
			
	def performActions(self, actions):
		for verb, addr, parms in actions:
			print("Action: %s %d %s" % (verb, addr, ", ".join(parms)))
			if verb == "outon":
				self.server.setOutputOn(addr, parms[0])
			elif verb == "outoff":
				self.server.setOutputOff(addr, parms[0])
			elif verb == "normal":
				self.server.setTurnoutNormal(addr, parms[0])
			elif verb == "reverse":
				self.server.setTurnoutReverse(addr, parms[0])
			elif verb == "toggle":
				self.server.setTurnoutToggle(addr, parms[0])
			elif verb == "angle":
				self.server.setServoAngle(addr, parms[0], parms[1])
			else:
				print("Unknown action verb: (%s)" % verb)
			
