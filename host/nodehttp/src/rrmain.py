from node import Node
from httpserver import JMRIHTTPServer
import json
import queue
import threading

class JMRIMain:
	def __init__(self, cfgfn):
		self.cfgfn = cfgfn
		with open(cfgfn, "r") as fp:
			self.cfg = json.load(fp)

		print(json.dumps(self.cfg, sort_keys=True, indent=4))
		
		print(self.cfg["port"])
		self.nodes = {}
		self.inputMaps = {}
		self.nodeCfg = {}
		for n in self.cfg["nodes"]:
			print("Configuring node: %s" % n["name"])
			ad = n["address"]
			if ad in self.nodes:
				print("Node address %d is already in use - skipping" % ad)
			else:
				node = Node()
				node.registerCallback(None, self.firstIdentityRcvd, None, None, None)
				node.connect(n["port"], n["baud"])
				node.getIdentity()
				node.start(poll=False)
				self.nodes[n["address"]] = node
			
		self.startHttpServer(self.cfg["port"])
		
	def process(self):
		self.HTTPProcess()
		for n in self.nodes:
			self.nodes[n].process()
		
	def firstIdentityRcvd(self, addr, inp, outp, servo):
		print("first identity received")
		if addr not in self.nodes:
			print("address in identity report (%d) is not defined" % addr)
			return
		node = self.nodes[addr]
		self.inputMaps[addr] = [True] * (inp*8)
		self.nodeCfg[addr] = (inp, outp, servo)
		node.configure(addr, inp, outp, servo)
		node.registerCallback(self.inputRcvd, self.identityRcvd, self.getTurnoutRcvd, self.storeRcvd, self.msgRcvd)
		node.setPoll(True)
		node.getCurrentInput()

	def inputRcvd(self, addr, vals, delta):
		print("addr %d vals %s delta %s" % (addr, str(vals), str(delta)))
		map = self.inputMaps[addr]
		for inp, val in vals:
			map[inp] = val == 1
	
	def identityRcvd(self, addr, inp, outp, servo):
		msg = "Configuration received:\n  Addr: %d" % addr
		msg += "  Inputs: %d - %d channels\n" % (inp, inp*8)
		msg += "  Outputs: %d - %d channels\n" % (outp, outp*8)
		msg += "  Servos: %d - %d channels\n" % (servo, servo*16)	
		print(msg)
			
	def getTurnoutRcvd(self, addr, tx, norm, rev, ini):
		print("Turnout %d:%d:\n Normal: %d\n Reverse: %d\n Initial: %d" % (addr, tx, norm, rev, ini))
			
	def storeRcvd(self, addr, res):
		print("store from addr %d" % addr)
		for i in range(0, len(res), 3):
			print("Turnout %d: %d/%d/%d" % (int(i/3), res[i], res[i+1], res[i+2]))

	def msgRcvd(self, addr, cmd, msg):
		s = "RCV  %d %02x: " % (addr, ord(cmd))   
		for c in msg:
			s += "%02x " % c
		print(s)
			
	def HTTPProcess(self):
		while not self.HttpCmdQ.empty():
			try:
				cmd = self.HttpCmdQ.get(False)
			except queue.Empty:
				cmd = None

			print("cmd(%s)" % str(cmd))

			if cmd is None:
				return 

			
			terms = cmd.split(":")
			print("terms: %s" % str(terms))
			verb = terms[0]
			if len(terms) > 1:
				parms = terms[1:]
			else:
				parms = []
			print("verb(%s)" % verb)
			print("parms: %s" % str(parms))

			if verb in ["tr", "tn"]:
				if len(parms) != 2:
					self.HttpRespQ.put((400, b'invalid number of parameters: 2 required'))
					continue

				try:
					addr = int(parms[0])
				except:
					self.HttpRespQ.put((400, b'unknown node address'))
					continue
					
				if addr not in self.nodes:
					self.HttpRespQ.put((400, b'unknown node address'))
					continue

				node = self.nodes[addr]

				try:
					tx = int(parms[1])
				except:
					self.HttpRespQ.put((400, b'invalid value for turnout number'))
					continue

				if tx < 0 or tx >= (node.servos*16):
					self.HttpRespQ.put((400, b'turnout number out of range'))
					continue

				if verb == "tr":
					node.setTurnoutReverse(tx)
				else:
					node.setTurnoutNormal(tx)
				self.HttpRespQ.put((200, b'command performed'))

			elif verb == "sa":
				if len(parms) != 3:
					self.HttpRespQ.put((400, b'invalid number of parameters: 3 required'))
					continue

				try:
					addr = int(parms[0])
				except:
					self.HttpRespQ.put((400, b'unknown node address'))
					continue
					
				if addr not in self.nodes:
					self.HttpRespQ.put((400, b'unknown node address'))
					continue

				node = self.nodes[addr]

				try:
					sx = int(parms[1])
				except:
					self.HttpRespQ.put((400, b'invalid value for servo number'))
					continue

				if sx < 0 or sx >= (node.servos*16):
					self.HttpRespQ.put((400, b'servo number out of range'))
					continue

				try:
					ang = int(parms[1])
				except:
					self.HttpRespQ.put((400, b'invalid value for servo angle'))
					continue

				if ang < 0 or ang > 180:
					self.HttpRespQ.put((400, b'angle out of range'))
					continue

				node.setAngle(sx, ang)
				self.HttpRespQ.put((200, b'command performed'))

			elif verb in ["of", "on"]:
				if len(parms) != 2:
					self.HttpRespQ.put((400, b'invalid number of parameters: 2 required'))
					continue

				try:
					addr = int(parms[0])
				except:
					self.HttpRespQ.put((400, b'unknown node address'))
					continue

				if addr not in self.nodes:
					self.HttpRespQ.put((400, b'unknown node address'))
					continue

				node = self.nodes[addr]

				try:
					ox = int(parms[1])
				except:
					self.HttpRespQ.put((400, b'invalid value for output number'))
					continue

				if ox < 0 or ox >= (node.outputs*8):
					self.HttpRespQ.put((400, b'output number out of range'))
					continue

				if verb == "of":
					node.setOutputOff(ox)
				else:
					node.setOutputOn(ox)
				self.HttpRespQ.put((200, b'command performed'))

			elif verb == "ic":
				if len(parms) != 1:
					self.HttpRespQ.put((400, b'invalid number of parameters: 1 required'))
					continue

				try:
					addr = int(parms[0])
				except:
					self.HttpRespQ.put((400, b'unknown node address'))
					continue

				if addr not in self.nodes:
					self.HttpRespQ.put((400, b'unknown node address'))
					continue

				resp = str(self.inputMaps[addr])
				self.HttpRespQ.put((200, resp.encode()))

			elif verb == "QUIT":
				self.HttpRespQ.put((200, b'command accepted'))
				self.serving = False
				
			else:
				self.HttpRespQ.put((400, b'bad request'))

	def startHttpServer(self, port):
		self.HttpCmdQ = queue.Queue(0)
		self.HttpRespQ = queue.Queue(0)
		self.serving = True
		self.jmriserver = JMRIHTTPServer(port, self.HttpCmdQ, self.HttpRespQ)

	def disconnectNodes(self):
		for n in self.nodes:
			node = self.nodes[n]
			try:
				node.stop()
				node.disconnect()

			except:
				pass

	def stopHttpServer(self):
		self.jmriserver.close()
		self.jmriserver.getThread().join()
		
	def serve_forever(self, interval):
		ticker = threading.Event()
		while not ticker.wait(interval) and self.serving:
			if self.serving:
				self.process()
		ticker = None
		print("Stopping HTTP Server...")
		self.stopHttpServer()

		print("disconnecting nodes...")
		self.disconnectNodes()

		print("exiting...")

jmri = JMRIMain("jmri.json")
jmri.serve_forever(0.25)

