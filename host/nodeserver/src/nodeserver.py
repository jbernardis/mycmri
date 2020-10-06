#!/usr/bin/env python3

from bus import Bus
from httpserver import NodeHTTPServer
from sktserver import SktServer
from nodetypes import ERRORRESPONSE, WARNINGRESPONSE
from nodeexceptions import NodeException

import json
import queue
import threading
import logging

class NodeServerMain:
	def __init__(self, cfgfn):
		logging.basicConfig(filename='nodeserver.log',
						filemode='w',
						format='%(asctime)s - %(levelname)s - %(message)s',
						level=logging.INFO)		
		self.cfgfn = cfgfn
		with open(cfgfn, "r") as fp:
			self.cfg = json.load(fp)
			
		logging.info("configuration loaded: " + json.dumps(self.cfg, sort_keys=True, indent=4))
		
		self.inputsMap = {}
		self.outputsMap = {}
		self.servosMap = {}
		self.nodeCfg = {}
		self.awaitingInitialIdentity = {}
		self.createSocketServer = True
		nodes = []
		if "nodes" not in self.cfg:
			logging.error("Configuration file does not have any nodes defined - exiting")
			exit(1)

		if "ip" not in self.cfg:
			logging.error("Configuration file does not specify an ip address for http server - exiting")
			exit(1)

		if "httpport" not in self.cfg:
			logging.error("Configuration file does not specify an port for http server - exiting")
			exit(1)

		if "socketport" not in self.cfg:
			logging.warning("Configuration file does not define socket port. No server will be created.")
			self.createSocketServer = False

		if "tty" not in self.cfg:
			logging.error("Configuration file does not specify a tty device for rs485 connection - exiting")
			exit(1)

		if "baud" not in self.cfg:
			logging.error("Configuration file does not specify baud rate for rs485 bus - exiting")
			exit(1)

		self.bus = Bus()
		self.bus.registerIdentityCallback(self.identityRcvd)
		self.bus.registerInputCallback(self.inputRcvd)
		self.bus.registerOutputCallback(self.outputRcvd)
		self.bus.registerTurnoutCallback(self.turnoutRcvd)
		self.bus.registerIdentityCallback(self.identityRcvd)
		self.bus.registerDefaultCallback(self.msgRcvd)
		tty = self.cfg["tty"]
		baud = self.cfg["baud"]
		try:
			self.bus.connect(tty, baud)
		except NodeException:
			logging.error("Unable to open port %s - exiting" % tty)
			exit(1)
		
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
				
			if ad <= 0:
				logging.error("Invalid node address - must be > 0 - exiting")
				exit(1)
				

			try:
				inp = n["inputs"]
				outp = n["outputs"]
				servo = n["servos"]
				nm = n["name"]
			except KeyError:
				logging.error("Node %s missing parameters - inputs, outputs, servos, name all required - exiting")
				exit(1)

			if ad in self.nodeCfg:
				logging.error("Node %d is already defined - skipping" % ad)
			else:
				self.nodeCfg[ad] = (nm, inp, outp, servo)
				self.inputsMap[ad] = [True] * (inp*8)		
				self.outputsMap[ad] = [False] * (outp*8)
				self.servosMap[ad] = [[0, 0, 0, 0]] * (servo*16)
				nodes.append([ad, inp])
			
		self.bus.start([a[0] for a in nodes])
		for ad in self.nodeCfg:
			self.startNode(ad)
			
		self.startHttpServer(self.cfg["ip"], self.cfg["httpport"])
		if self.createSocketServer:
			self.socketServer = SktServer(self.cfg["ip"], self.cfg["socketport"])
			self.socketServer.start()
			
	def startNode(self, addr):
		self.awaitingInitialIdentity[addr] = True
		self.bus.getIdentity(addr)		
		
	def process(self):
		self.HTTPProcess()
		self.bus.process()
		
	def identityRcvd(self, addr, inp, outp, servo):
		msg = "Configuration received:\n  Addr: %d" % addr
		msg += "  Inputs: %d - %d channels\n" % (inp, inp*8)
		msg += "  Outputs: %d - %d channels\n" % (outp, outp*8)
		msg += "  Servos: %d - %d channels\n" % (servo, servo*16)	
		logging.info(msg)

		# things to do the first time through		
		if self.awaitingInitialIdentity[addr]:
			self.awaitingInitialIdentity[addr] = False
			self.inputsMap[addr] = [True] * (inp*8)		
			self.outputsMap[addr] = [False] * (outp*8)
			self.servosMap[addr] = [[0, 0, 0, 0]] * (servo*16)
			
			nm = self.nodeCfg[addr][0]
			self.nodeCfg[addr] = (nm, inp, outp, servo)
			self.bus.setPoll(addr, True)
			self.bus.getCurrentInput(addr)
			self.bus.getCurrentOutput(addr)
			self.bus.getTurnouts(addr)

	def inputRcvd(self, addr, vals, delta):
		if len(vals) == 0:
			return 
		
		for inp, val in vals:
			self.inputsMap[addr][inp] = val == 1
			
		if self.createSocketServer:
			s = json.dumps({"addr": addr, "type": "input", "values": vals, "delta": delta})
			self.socketServer.sendToAll(s.encode())

		if not delta:
			rpt = "Current input report for addr %d\n" % addr
			
			i = 0
			for inp, val in vals:
				rpt +="    %2d: %s" % (inp, str(val==1))
				i += 1
				if i % 4 == 0:
					rpt += "\n"
			logging.info(rpt)
			
		else: # delta is true
			rpt = "Delta input report for addr %d" % addr
			
			i = 0
			for inp, val in vals:
				rpt += "    %2d: %s" % (inp, str(val==1))
				i += 1
				if i % 4 == 0:
					rpt += "\n"
			logging.info(rpt)
				
	def setTurnoutNormal(self, addr, tx):
		logging.info("  Normal turnout %d:%d" % (addr, tx))
		self.bus.setTurnoutNormal(addr, tx)
		self.servosMap[addr][tx][3] = self.servosMap[addr][tx][0]
		if self.createSocketServer:
			s = json.dumps({"addr": addr, "type": "turnout", "values": self.servosMap[addr]})
			self.socketServer.sendToAll(s.encode())

	def setTurnoutReverse(self, addr, tx):
		logging.info("  Reverse turnout %d:%d" % (addr, tx))
		self.bus.setTurnoutReverse(addr, tx)
		self.servosMap[addr][tx][3] = self.servosMap[addr][tx][1]
		if self.createSocketServer:
			s = json.dumps({"addr": addr, "type": "turnout", "values": self.servosMap[addr]})
			self.socketServer.sendToAll(s.encode())
		
	def setOutputOn(self, addr, ox):
		logging.info("  Output %d:%d ON" % (addr, ox))
		self.bus.setOutputOn(addr, ox)
		self.outputsMap[addr][ox] = True
		if self.createSocketServer:
			s = json.dumps({"addr": addr, "type": "output", "values": self.outputsMap[addr]})
			self.socketServer.sendToAll(s.encode())
		
	def setOutputOff(self, addr, ox):
		logging.info("  Output %d:%d OFF" % (addr, ox))
		self.bus.setOutputOff(addr, ox)
		self.outputsMap[addr][ox] = False
		if self.createSocketServer:
			s = json.dumps({"addr": addr, "type": "output", "values": self.outputsMap[addr]})
			self.socketServer.sendToAll(s.encode())

	def setAngle(self, addr, sx, ang):
		logging.info("  Servo %d:%d to angle %d" % (addr, sx, ang))
		self.bus.setAngle(addr, sx, ang)
		self.servosMap[addr][sx][3] = ang
		if self.createSocketServer:
			s = json.dumps({"addr": addr, "type": "turnout", "values": self.servosMap[addr]})
			self.socketServer.sendToAll(s.encode())

	def setTurnoutLimits(self, addr, tx, norm, rev, ini):		
		self.bus.setTurnoutLimits(addr, tx, norm, rev, ini)
		self.servosMap[addr][tx][0] = norm
		self.servosMap[addr][tx][1] = rev
		self.servosMap[addr][tx][2] = ini
		if self.createSocketServer:
			s = json.dumps({"addr": addr, "type": "turnout", "values": self.servosMap[addr]})
			self.socketServer.sendToAll(s.encode())
		
	def setConfig(self, addr, naddr, inputs, outputs, servos):
		self.bus.setConfig(addr, naddr, inputs, outputs, servos)

	def outputRcvd(self, addr, vals):
		rpt = "Output report for addr %d" % addr
		omap = self.outputsMap[addr]
		for i in range(len(vals)):
			omap[i] = vals[i]==1
			rpt += "    %2d: %s" % (i, vals[i]==1)
			if (i+1) % 4 == 0:
				rpt += "\n"
		logging.info(rpt)
		if self.createSocketServer:
			s = json.dumps({"addr": addr, "type": "output", "values": self.outputsMap[addr]})
			self.socketServer.sendToAll(s.encode())
			
	def turnoutRcvd(self, addr, vals):
		rpt = "Turnout report for address %d: (norm, rev, ini, cur)" % addr
		tmap= self.servosMap[addr]
		for i in range(len(vals)):
			v = vals[i]
			tmap[i] = v
			rpt += "    %2d: %3d/%3d/%3d/%3d" % (i, v[0], v[1], v[2], v[3])
			if (i+1) % 4 == 0:
				rpt += "\n"
		logging.info(rpt)
		if self.createSocketServer:
			s = json.dumps({"addr": addr, "type": "turnout", "values": self.servosMap[addr]})
			self.socketServer.sendToAll(s.encode())

	def msgRcvd(self, addr, cmd, msg):
		if cmd == ERRORRESPONSE:
			logging.error("Error from node at address %d: %s" % (addr, msg))
			if self.awaitingInitialIdentity[addr]:
				logging.error("This node has not responded with initial identity")
		elif cmd == WARNINGRESPONSE:
			logging.error("Warning from node at address %d: %s" % (addr, msg))
			if self.awaitingInitialIdentity[addr]:
				logging.error("This node has not responded with initial identity")
		else:
			s = "Unknown message received from address %d %02x: " % (addr, ord(cmd))   
			for c in msg:
				s += "%02x " % ord(c)
			logging.error(s)	
			
	def HTTPProcess(self):
		while not self.HttpCmdQ.empty():
			try:
				cmd = self.HttpCmdQ.get(False)
			except queue.Empty:
				cmd = None

			if cmd is None:
				return 

			try:
				verb = cmd["cmd"][0]
			except KeyError:
				self.HttpRespQ.put((400, b'missing verb'))
				continue
			except:
				self.HttpRespQ.put((400, b'unexpected error retrieving command'))
				continue

			if not verb in ["quit", "noderpt"]:
				try:
					addr = int(cmd["addr"][0])
				except KeyError:
					self.HttpRespQ.put((400, b'missing bus address'))
					continue
				except ValueError:
					self.HttpRespQ.put((400, b'ill-formed bus address'))
					continue
				except:
					self.HttpRespQ.put((400, b'unexpected error retrieving bus address'))
					continue
				
				if addr not in self.nodeCfg:
					self.HttpRespQ.put((400, b'unknown node address'))
					continue
				
				if verb == "init":
					self.startNode(addr)
					self.HttpRespQ.put((200, b'command accepted'))
					continue
				
				if addr not in self.awaitingInitialIdentity or self.awaitingInitialIdentity[addr]:
					msg = "communications with node %d has not been established" % addr
					self.HttpRespQ.put((400, msg.encode()))
					continue
				
				_, _, outp, servo = self.nodeCfg[addr]
			else:
				addr = None

			if verb in ["reverse", "normal"]:
				try:
					tx = int(cmd["index"][0])
				except KeyError:
					self.HttpRespQ.put((400, b'missing turnout index'))
					continue
				except ValueError:
					self.HttpRespQ.put((400, b'invalid value for turnout index'))
					continue
				except:
					self.HttpRespQ.put((400, b'unexpected error retrieving turnout index'))
					continue

				if tx < 0 or tx >= (servo*16):
					self.HttpRespQ.put((400, b'turnout index out of range'))
					continue

				if verb == "reverse":
					self.setTurnoutReverse(addr, tx)
				else:
					self.setTurnoutNormal(addr, tx)
				self.HttpRespQ.put((200, b'command performed'))


			elif verb == "angle":
				try:
					sx = int(cmd["index"][0])
				except KeyError:
					self.HttpRespQ.put((400, b'missing servo index'))
					continue
				except ValueError:
					self.HttpRespQ.put((400, b'invalid value for servo index'))
					continue
				except:
					self.HttpRespQ.put((400, b'unexpected error retrieving servo index'))
					continue

				if sx < 0 or sx >= (servo*16):
					self.HttpRespQ.put((400, b'servo index out of range'))
					continue

				try:
					ang = int(cmd["angle"][0])
				except KeyError:
					self.HttpRespQ.put((400, b'missing servo angle'))
					continue
				except ValueError:
					self.HttpRespQ.put((400, b'invalid value for servo angle'))
					continue
				except:
					self.HttpRespQ.put((400, b'unexpected error retrieving servo angle'))
					continue

				if ang < 0 or ang > 180:
					self.HttpRespQ.put((400, b'angle out of range'))
					continue

				self.setAngle(addr, sx, ang)
				self.HttpRespQ.put((200, b'command performed'))

			elif verb in ["outoff", "outon"]:
				try:
					ox = int(cmd["index"][0])
				except KeyError:
					self.HttpRespQ.put((400, b'missing output index'))
					continue
				except ValueError:
					self.HttpRespQ.put((400, b'invalid value for output number'))
					continue
				except:
					self.HttpRespQ.put((400, b'unexpected error retrieving output index'))
					continue

				if ox < 0 or ox >= (outp*8):
					self.HttpRespQ.put((400, b'output index out of range'))
					continue

				if verb == "outoff":
					self.setOutputOff(addr, ox)
				else:
					self.setOutputOn(addr, ox)
				self.HttpRespQ.put((200, b'command performed'))

			elif verb in ["inputs", "outputs", "turnouts", "getconfig"]:
				if verb == "inputs":
					resp = str(self.inputsMap[addr])
				elif verb == "outputs":
					resp = str(self.outputsMap[addr])
				elif verb == "turnouts":
					resp = str(self.servosMap[addr])
				else: # verb == "getconfig"
					resp = str(self.nodeCfg[addr])
					
				self.HttpRespQ.put((200, resp.encode()))

			elif verb == "refresh":
				self.bus.getCurrentInput(addr)
				self.bus.getCurrentOutput(addr)
				self.bus.getTurnouts(addr)
				self.HttpRespQ.put((200, b'command accepted'))

			elif verb == "setlimits":
				try:
					tx = int(cmd["index"][0])
				except KeyError:
					self.HttpRespQ.put((400, b'missing turnout index'))
					continue
				except ValueError:
					self.HttpRespQ.put((400, b'invalid value for turnout index'))
					continue
				except:
					self.HttpRespQ.put((400, b'unexpected error retrieving turnout index'))
					continue

				if tx < 0 or tx >= (servo*16):
					self.HttpRespQ.put((400, b'turnout index out of range'))
					continue

				try:
					norm = int(cmd["normal"][0])
				except KeyError:
					self.HttpRespQ.put((400, b'missing normal angle'))
					continue
				except ValueError:
					self.HttpRespQ.put((400, b'invalid value for normal angle'))
					continue
				except:
					self.HttpRespQ.put((400, b'unexpected error retrieving normal angle'))
					continue

				if norm < 0 or norm > 180:
					self.HttpRespQ.put((400, b'normal angle out of range'))
					continue
				
				try:
					rev = int(cmd["reverse"][0])
				except KeyError:
					self.HttpRespQ.put((400, b'missing reverse angle'))
					continue
				except ValueError:
					self.HttpRespQ.put((400, b'invalid value for reverse angle'))
					continue
				except:
					self.HttpRespQ.put((400, b'unexpected error retrieving reverse angle'))
					continue

				if rev < 0 or rev > 180:
					self.HttpRespQ.put((400, b'reverse angle out of range'))
					continue
				
				try:
					ini = int(cmd["initial"][0])
				except KeyError:
					ini = norm
				except ValueError:
					self.HttpRespQ.put((400, b'invalid value for initial angle'))
					continue
				except:
					self.HttpRespQ.put((400, b'unexpected error retrieving initial angle'))
					continue

				if ini < 0 or ini > 180:
					self.HttpRespQ.put((400, b'initial angle out of range'))
					continue

				self.setTurnoutLimits(addr, tx, norm, rev, ini)
				self.HttpRespQ.put((200, b'command performed'))

			elif verb == "setconfig":
				try:
					naddr = int(cmd["naddr"][0])
				except KeyError:
					self.HttpRespQ.put((400, b'missing new address'))
					continue
				except ValueError:
					self.HttpRespQ.put((400, b'invalid value for new node address'))
					continue
				except:
					self.HttpRespQ.put((400, b'unexpected error retrieving new address'))
					continue

				if naddr < 1 or naddr > 99:
					self.HttpRespQ.put((400, b'new address out of range'))
					continue

				try:
					inputs = int(cmd["inputs"][0])
				except KeyError:
					self.HttpRespQ.put((400, b'missing inputs'))
					continue
				except ValueError:
					self.HttpRespQ.put((400, b'invalid value for inputs'))
					continue
				except:
					self.HttpRespQ.put((400, b'unexpected error retrieving inputs'))
					continue

				if inputs < 0 or inputs > 7:
					self.HttpRespQ.put((400, b'inputs out of range'))
					continue

				try:
					outputs = int(cmd["outputs"][0])
				except KeyError:
					self.HttpRespQ.put((400, b'missing outputs'))
					continue
				except ValueError:
					self.HttpRespQ.put((400, b'invalid value for outputs'))
					continue
				except:
					self.HttpRespQ.put((400, b'unexpected error retrieving outputs'))
					continue

				if outputs < 0 or outputs > 7:
					self.HttpRespQ.put((400, b'outputs out of range'))
					continue

				try:
					servos = int(cmd["servos"][0])
				except KeyError:
					self.HttpRespQ.put((400, b'missing servos'))
					continue
				except ValueError:
					self.HttpRespQ.put((400, b'invalid value for servos'))
					continue
				except:
					self.HttpRespQ.put((400, b'unexpected error retrieving servos'))
					continue

				if servos < 0 or servos > 7:
					self.HttpRespQ.put((400, b'servos out of range'))
					continue

				self.setConfig(addr, naddr, inputs, outputs, servos)
				self.HttpRespQ.put((200, b'command performed'))

			elif verb == "noderpt":
				result = "{"
				first = True
				for n in self.nodeCfg:
					if not first:
						result += ", "
					first = False
					cfg = self.nodeCfg[n]
					try:
						active = not self.awaitingInitialIdentity[n]
					except:
						active = False
					result += "'%s': {'addr': %d, 'input': %d, 'output': %d, 'servo': %d, 'active': %s} " % (cfg[0], n, cfg[1], cfg[2], cfg[3], active)
				result += "}"
				
				self.HttpRespQ.put((200, result.encode()))

			elif verb == "store":
				self.bus.store(addr)
				
				self.HttpRespQ.put((200, b'command accepted'))

			elif verb == "quit":
				self.HttpRespQ.put((200, b'command accepted'))
				self.serving = False
				
			else:
				self.HttpRespQ.put((400, b'bad request'))

	def startHttpServer(self, ip, port):
		logging.info("Starting HTTP server at address: %s:%d" % (ip, port))
		self.HttpCmdQ = queue.Queue(0)
		self.HttpRespQ = queue.Queue(0)
		self.serving = True
		self.nodeserver = NodeHTTPServer(ip, port, self.HttpCmdQ, self.HttpRespQ)

	def disconnectNodes(self):
			try:
				self.bus.stop()
				self.bus.disconnect()

			except:
				pass

	def stopHttpServer(self):
		self.nodeserver.close()
		self.nodeserver.getThread().join()
		
	def serve_forever(self, interval):
		ticker = threading.Event()
		while not ticker.wait(interval) and self.serving:
			if self.serving:
				self.process()
		ticker = None
		logging.info("Stopping HTTP Server...")
		self.stopHttpServer()
		
		if self.createSocketServer:	
			logging.info("Stopping socket server...")
			self.socketServer.kill()

		logging.info("disconnecting nodes...")
		self.disconnectNodes()

		logging.info("exiting...")

node = NodeServerMain("nodecfg.json")
node.serve_forever(0.25)

