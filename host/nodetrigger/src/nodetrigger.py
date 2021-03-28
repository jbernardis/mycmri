#!/usr/bin/env python3

from triggertable import TriggerTable
from listener import Listener
from server import Server
from config import NodeConfig

import json
import logging
import queue

class NodeTrigger:
	def __init__(self, cfgfn):
		logging.basicConfig(filename='nodetrigger.log',
						filemode='w',
						format='%(asctime)s - %(levelname)s - %(message)s',
						level=logging.INFO)	
		
		self.cfg = NodeConfig(cfgfn).load()
		if self.cfg is None:
			logging.error("unable to load configuration file: %s" % cfgfn)
			exit(1)
			
		logging.info("configuration loaded: " + json.dumps(self.cfg, sort_keys=True, indent=4))
		
		if "nodes" not in self.cfg:
			logging.error("Configuration file does not have any nodes defined - exiting")
			exit(1)

		if "ip" not in self.cfg:
			logging.error("Configuration file does not specify an ip address for node server - exiting")
			exit(1)

		if "httpport" not in self.cfg:
			logging.error("Configuration file does not specify an port for node server - exiting")
			exit(1)

		if "socketport" not in self.cfg:
			logging.warning("Configuration file does not define socket port. No server will be created.")
			self.createSocketServer = False

		nodes = []
		self.inputs = {}
		self.outputs = {}
		self.flags = {}
		self.registers = {}
		
		for n in self.cfg["nodes"]:
			try:
				logging.info("Configuring node: %s" % n["name"])
			except KeyError:
				logging.error("Node name not specified - exiting")
				exit(1)
				
			try:
				ad = n["address"]
			except KeyError:
				logging.error("Node %d does not specify an address - exiting" % n["name"])
				exit(1)

			try:
				inp = n["inputs"]
			except KeyError:
				logging.error("Node %s missing inputs parameters - exiting")
				exit(1)

			try:
				outp = n["outputs"]
			except KeyError:
				logging.error("Node %s missing outputs parameters - exiting")
				exit(1)
				
			try:				
				nflags = n["flags"]
			except KeyError:
				nflags = 0
				
			try:
				nregisters = n["registers"]
			except KeyError:
				nregisters = 0


			nodes.append([ad, inp, outp, nflags, nregisters])
			self.inputs[ad] = [True for _ in range(inp*8)]
			self.outputs[ad] = [True for _ in range(outp*8)]
			self.flags[ad] = [False for _ in range(nflags)]
			self.registers[ad] = ["" for _ in range(nregisters)]
		
		self.triggerTable = TriggerTable(nodes)
		
		self.server = Server()
		self.server.setServerAddress(self.cfg["ip"], self.cfg["httpport"])
		logging.info("Node server address set to %s:%s" % (self.cfg["ip"], self.cfg["httpport"]))
		
		self.msgQ = queue.Queue(0)
		self.listener = Listener(self, self.cfg["ip"], self.cfg["socketport"], self.msgQ)
		self.listener.start()
		logging.info("Listener started at address %s:%s" % (self.cfg["ip"], self.cfg["socketport"]))
		
	def serve_forever(self):
		self.forever = True
		while self.forever:
			try:
				msg = self.msgQ.get(True, 0.25)
			except queue.Empty:
				msg = None
			
			if msg:
				jdata = json.loads(msg)
				if jdata["type"] == "disconnect":
					logging.info("server has disconnected - exiting")
					self.forever = False
					
				elif jdata["type"] == "input":
					self.inputRcvd(jdata["addr"], jdata["values"], jdata["delta"])
					
				elif jdata["type"] == "output":
					self.outputRcvd(jdata["addr"], jdata["values"])
					
				elif jdata["type"] == "flags":
					self.flagsRcvd(jdata["addr"], jdata["values"])
					
				elif jdata["type"] == "registers":
					self.registersRcvd(jdata["addr"], jdata["values"])
					
		logging.info("joining with listener thread")
		self.listener.join()
			
	def inputRcvd(self, addr, vals, deltaRpt):
		if not deltaRpt:
			delta = False
			for inp, val in vals:
				nv = val == 1
				if self.inputs[addr[inp]] != nv:
					self.inputs[addr][inp] = nv
					delta = True
					
			rpt = "Current input report for addr %d\n" % addr
			
			i = 0
			for inp, val in vals:
				rpt +="    %2d: %s" % (inp, str(val==1))
				i += 1
				if i % 4 == 0:
					rpt += "\n"
			logging.info(rpt)
			
			self.triggerTable.updateInputs(addr, self.inputs[addr])
			
		else: # deltaRpt is true
			delta = True
			for inp, val in vals:
				self.inputs[addr][inp] = val == 1
			if len(vals) == 0:
				return
			
			rpt = "Delta input report for addr %d\n" % addr
			
			i = 0
			for inp, val in vals:
				self.triggerTable.updateInput(addr, inp, val == 1)
				rpt += "    %2d: %s" % (inp, str(val==1))
				i += 1
				if i % 4 == 0:
					rpt += "\n"
			logging.info(rpt)
			
		if delta:
			self.checkTriggers(addr)
			
	def outputRcvd(self, addr, vals):
		delta = False
		print("Output Rcvd: %d (%s)" % (addr, str(vals)))
		for i in range(len(vals)):
			if self.outputs[addr][i] != vals[i]:
				self.outputs[addr][i] = vals[i]
				delta = True

		rpt = "Current outputs report for addr %d\n" % addr
		
		for i in range(len(vals)):
			rpt +="    %2d: %s" % (i, vals[i])
			if i % 4 == 0:
				rpt += "\n"
		logging.info(rpt)
		
		self.triggerTable.updateOutputs(addr, self.outputs)
			
	def flagsRcvd(self, addr, vals):
		delta = False
		print("Flags Rcvd: %d (%s)" % (addr, str(vals)))
		for i in range(len(vals)):
			if self.flags[addr][i] != vals[i]:
				self.flags[addr][i] = vals[i]
				delta = True

		rpt = "Current flags report for addr %d\n" % addr
		
		for i in range(len(vals)):
			rpt +="    %2d: %s" % (i, vals[i])
			if i % 4 == 0:
				rpt += "\n"
		logging.info(rpt)
		
		self.triggerTable.updateFlags(addr, self.flags)
		
	def registersRcvd(self, addr, vals):
		delta = False
		for i in range(len(vals)):
			if self.registers[addr][i] != vals[i]:
				self.registers[addr][i] = vals[i]
				delta = True

		rpt = "Current registers report for addr %d\n" % addr
		
		for i in range(len(vals)):
			rpt +="    %2d: %s" % (i, vals[i])
			if i % 4 == 0:
				rpt += "\n"
		logging.info(rpt)
		
		self.triggerTable.updateRegisters(addr, self.registers)
		
	def checkTriggers(self, addr):
		logging.info("check for triggers")
		actions = self.triggerTable.checkTriggers(addr)
		
		if len(actions) == 0:
			logging.info("No actions triggered")
		else:
			logging.info("%d Triggered actions" % len(actions))
			for a in actions:
				self.performAction(a[0], a[1], a[2])
					
	def performAction(self, verb, addr, params):
		logging.info("Performing action: %s %s %s" % (verb, addr, str(params)))
		if verb == "normal":
			self.server.setTurnoutNormal(addr, params[0])

		elif verb == "reverse":
			self.server.setTurnoutReverse(addr, params[0])

		elif verb == "toggle":
			self.server.setTurnoutToggle(addr, params[0])

		elif verb == "angle":
			self.server.setServoAngle(addr, params[0], params[1])

		elif verb == "outon":
			self.server.setOutputOn(addr, params[0])
			
		elif verb == "outoff":
			self.server.setOutputOff(addr, params[0])
			
		elif verb == "flagon":
			self.server.setFlag(addr, params[0])
			
		elif verb == "flagoff":
			self.server.clearFlag(addr, params[0])
			
		elif verb == "register":
			self.server.setRegister(addr, params[0], params[1])

		else:
			logging.error("Unknown action verb: %s" % verb)

node = NodeTrigger("nodecfg.json")
node.serve_forever()
logging.info("exiting")

