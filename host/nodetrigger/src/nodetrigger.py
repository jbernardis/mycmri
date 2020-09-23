#!/usr/bin/env python3

from triggertable import TriggerTable
from listener import Listener

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
			logging.error("Configuration file does not specify an ip address for http server - exiting")
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
		
		self.msgQ = queue.Queue(0)
		
		self.listener = Listener(self, self.cfg["ip"], self.cfg["socketport"], self.msgQ)
		self.listener.start()
		
	def serve_forever(self):
		self.forever = True
		while self.forever:
			try:
				msg = self.msgQ.get(True, 0.25)
			except queue.Empty:
				msg = None
			
			if msg:
				print("recvd: (%s)" % msg)
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
			print("Current input report for addr %d" % addr)
			
			i = 0
			for inp, val in vals:
				print("    %2d: %s" % (inp, str(val==1)), end="")
				i += 1
				if i % 4 == 0:
					print("")
			print("")
			
			self.triggerTable.updateInputs(addr, imap)
			
		else: # delta is true
			if len(vals) == 0:
				return
			
			print("Delta input report for addr %d" % addr)
			
			i = 0
			for inp, val in vals:
				self.triggerTable.updateInput(addr, inp, val == 1)
				print("    %2d: %s" % (inp, str(val==1)), end="")
				i += 1
				if i % 4 == 0:
					print("")
			print("")
				
			print("check for triggers")
			actions = self.triggerTable.checkInputTriggers(addr)
			
			if len(actions) == 0:
				print("No actions triggered")
			else:
				print("Triggered actions (%d):" % len(actions))
				for a in actions:
					print("Action: ", a[0], a[1], a[2:])
				print("")




jmri = JMRITrigger("jmri.json")
jmri.serve_forever()
logging.info("exiting")

