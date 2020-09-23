#!/usr/bin/env python3

from triggertable import TriggerTable
from listener import Listener
from server import Server

import json
import logging
import queue

class JMRITrigger:
	def __init__(self, cfgfn):
		self.cfgfn = cfgfn
		with open(cfgfn, "r") as fp:
			self.cfg = json.load(fp)

		logging.basicConfig(filename='jmritrigger.log',
						filemode='w',
						format='%(asctime)s - %(levelname)s - %(message)s',
						level=logging.INFO)	
			
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
		self.inputsMap = {}
		
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

			nodes.append([ad, inp])
			self.inputsMap[ad] = [True] * (inp*8)

		
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
					
		logging.info("joining with listener thread")
		self.listener.join()
			
	def inputRcvd(self, addr, vals, delta):
		imap = self.inputsMap[addr]
		
		for inp, val in vals:
			imap[inp] = val == 1

		if not delta:
			rpt = "Current input report for addr %d\n" % addr
			
			i = 0
			for inp, val in vals:
				rpt +="    %2d: %s" % (inp, str(val==1))
				i += 1
				if i % 4 == 0:
					rpt += "\n"
			logging.info(rpt)
			
			self.triggerTable.updateInputs(addr, imap)
			
		else: # delta is true
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
				
			logging.info("check for triggers")
			actions = self.triggerTable.checkInputTriggers(addr)
			
			if len(actions) == 0:
				logging.info("No actions triggered")
			else:
				logging.info("%d Triggered actions" % len(actions))
				for a in actions:
					self.performAction(a[0], a[1], a[2:])
					
	def performAction(self, verb, addr, params):
		logging.info("Performing action: %s %s %s" % (verb, addr, str(params)))
		if verb == "normal":
			self.server.setTurnoutNormal(addr, params[0])

		elif verb == "reverse":
			self.server.setTurnoutReverse(addr, params[0])

		elif verb == "angle":
			self.server.setServoAngle(addr, params[0], params[1])

		elif verb == "outon":
			self.server.setOutputOn(addr, params[0])
			
		elif verb == "outoff":
			self.server.setOutputOff(addr, params[0])
			
		else:
			logging.error("Unknown action verb: %s" % verb)

jmri = JMRITrigger("jmri.json")
jmri.serve_forever()
logging.info("exiting")

