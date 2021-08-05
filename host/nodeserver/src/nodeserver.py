#!/usr/local/bin/python3.8

from bus import Bus
from httpserver import NodeHTTPServer
from sktserver import SktServer
from nodetypes import ERRORRESPONSE, WARNINGRESPONSE
from node import Node
from nodeexceptions import NodeException
from config import NodeConfig

import json
import queue
import threading
import logging

import os, inspect
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))

ERROR_THRESHOLD = 5

class NodeServerMain:
	def __init__(self, cfgfn):
		self.cfg = NodeConfig(cmd_folder, cfgfn).load()
		if self.cfg is None:
			print("unable to load configuration file: %s/%s" % (cmd_folder, cfgfn))
			exit(1)
			
		print("configuration loaded: " + json.dumps(self.cfg, sort_keys=True, indent=4))
		
		self.nodes = {}
		self.errors = {}
		self.createSocketServer = True
		self.nodesToInit = {}
		nodesToPoll = []
		if "nodes" not in self.cfg:
			print("Configuration file does not have any nodes defined - exiting")
			exit(1)

		if "ip" not in self.cfg:
			print("Configuration file does not specify an ip address for http server - exiting")
			exit(1)

		if "httpport" not in self.cfg:
			print("Configuration file does not specify an port for http server - exiting")
			exit(1)

		if "socketport" not in self.cfg:
			print("Configuration file does not define socket port. No server will be created.")
			self.createSocketServer = False

		if "tty" not in self.cfg:
			print("Configuration file does not specify a tty device for rs485 connection - exiting")
			exit(1)

		if "baud" not in self.cfg:
			print("Configuration file does not specify baud rate for rs485 bus - exiting")
			exit(1)

		if "timeout" not in self.cfg:
			print("Configuration file does not specify bus timeout - defaulting to 1 second")
			self.cfg["timeout"] = 1

		if "logfile" not in self.cfg:
			logfile = os.path.join(cmd_folder, 'nodeserver.log')
			print("Configuration file does not specify logfile - using default value")
		else:
			logfile = self.cfg['logfile']
			
		print("Logs being written to %s" % logfile)


		logging.basicConfig(filename=logfile,
						filemode='w',
						format='%(asctime)s - %(levelname)s - %(message)s',
						level=logging.INFO)		
			
		self.bus = Bus()
		# self.bus.registerIdentityCallback(self.identityRcvd)
		self.bus.registerInputCallback(self.inputRcvd)
		self.bus.registerOutputCallback(self.outputRcvd)
		self.bus.registerTurnoutCallback(self.turnoutRcvd)
		self.bus.registerIdentityCallback(self.identityRcvd)
		self.bus.registerDefaultCallback(self.msgRcvd)
		tty = self.cfg["tty"]
		baud = self.cfg["baud"]
		timeout = self.cfg["timeout"]
		try:
			self.bus.connect(tty, baud, timeout)
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
				nm = n["name"]
			except KeyError:
				logging.error("Node %s missing name - exiting")
				exit(1)

			if ad in self.nodes:
				logging.error("Node %d is already defined - skipping" % ad)
			else:
				self.nodes[ad] = Node(ad, nm)
				self.errors[ad] = 0
				nodesToPoll.append(ad)
			
		self.bus.start(nodesToPoll)
		startTime = 10
		for ad in self.nodes:
			self.nodesToInit[ad] = startTime
			logging.info("starting node %d after %d cycles" % (ad, startTime))
			startTime += 10
			
		self.startHttpServer(self.cfg["ip"], self.cfg["httpport"])
		if self.createSocketServer:
			self.socketServer = SktServer(self.cfg["ip"], self.cfg["socketport"])
			self.socketServer.start()
			
	def startNode(self, addr):
		self.bus.setPoll(addr, True)
		self.bus.getIdentity(addr)		

	def stopNode(self, addr):
		self.bus.setPoll(addr, False)
		self.nodes[addr].stop()
		self.updateNodesRpt()
		
	def process(self):
		self.HTTPProcess()
		self.bus.process()
		ns = self.socketServer.getNewSockets()
		if ns is not None:
			rpt = self.nodesReport()
			for skt, saddr in ns:
				self.socketServer.sendToOne(skt, saddr, rpt)
			for ad in self.nodes:
				rpt = self.inputsReport(ad)
				for skt, saddr in ns:
					self.socketServer.sendToOne(skt, saddr, rpt)
				rpt = self.outputsReport(ad)
				for skt, saddr in ns:
					self.socketServer.sendToOne(skt, saddr, rpt)
				rpt = self.servosReport(ad)
				for skt, saddr in ns:
					self.socketServer.sendToOne(skt, saddr, rpt)
				
		for ad in self.nodes.keys():
			if self.errors[ad] > ERROR_THRESHOLD and not self.nodes[ad].isStopped():
				logging.error("Error threshold exceeded for node at address %s.  Stopping node" % ad)
				self.stopNode(ad)

		for ad in list(self.nodesToInit.keys()):
			self.nodesToInit[ad] -= 1
			if self.nodesToInit[ad] <= 0:
				del(self.nodesToInit[ad])
				logging.info("Starting node %d" % ad)
				self.startNode(ad)
		
	def identityRcvd(self, addr, inp, outp, servo):
		msg = "Configuration received:\n  Addr: %d" % addr
		msg += "  Inputs: %d - %d channels\n" % (inp, inp*8)
		msg += "  Outputs: %d - %d channels\n" % (outp, outp*8)
		msg += "  Servos: %d - %d channels\n" % (servo, servo*16)	
		logging.info(msg)
		self.errors[addr] = 0

		# things to do the first time through		
		if not self.nodes[addr].isInitialized():
			self.nodes[addr].setConfig(inp, outp, servo)
			self.bus.setPoll(addr, True)
			self.bus.getCurrentInput(addr)
			self.bus.getCurrentOutput(addr)
			self.bus.getTurnouts(addr)
			self.updateNodesRpt()

	def updateNodesRpt(self):
		rpt = self.nodesReport()
		
		rptj = json.loads(rpt)
		logEntry = "Nodes report:\n"
		logEntry += "  Name  Address  Inputs  Outputs  Servos  Active\n"
		for n in rptj["nodes"]:
			logEntry += ("10.10s     %4d    %4d    %4d   %s\n" % (n["name"], n["address"], n["inputs"], n["outputs"], n["servos"], n["active"]))			
		logging.info(logEntry+"\n")
		
		if self.createSocketServer:
			self.socketServer.sendToAll(rpt.encode())

	def inputRcvd(self, addr, vals, delta):
		self.errors[addr] = 0
		if len(vals) == 0:
			return 
		
		for inp, val in vals:
			self.nodes[addr].setInput(inp, val == 1)
				
		if self.createSocketServer:
			s = "{\"inputs\":{\"address\": %d, \"count\": %d, \"delta\": %s, \"values\":[" % (addr, len(vals), "true" if delta else "false")
			if delta:
				vstr = []
				for ix, iv in vals:
					vstr.append("[%d, %s]" % (ix, "true" if iv else "false"))
				s += ", ".join(vstr) + "]}}"
			else:
				vstr = []
				for i in vals:
					vstr.append("true" if i else "false")
				s += ", ".join(vstr) + "]}}"
				
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
		self.nodes[addr].setTurnoutNormal(tx)
		if self.createSocketServer:
			r = "{\"servos\": { \"address\": %d, \"delta\": true, \"count\": 1, \"values\":[" % addr 
			r += "[ %d, %d ]]}}" % (tx, self.nodes[addr].getTurnoutNormal(tx))
			self.socketServer.sendToAll(r)

	def setTurnoutReverse(self, addr, tx):
		logging.info("  Reverse turnout %d:%d" % (addr, tx))
		self.bus.setTurnoutReverse(addr, tx)
		self.nodes[addr].setTurnoutReverse(tx)
		if self.createSocketServer:
			r = "{\"servos\": { \"address\": %d, \"delta\": true, \"count\": 1, \"values\":[" % addr 
			r += "[ %d, %d ]]}}" % (tx, self.nodes[addr].getTurnoutReverse(tx))
			self.socketServer.sendToAll(r)

	def setTurnoutToggle(self, addr, tx):
		logging.info("  Toggle turnout %d:%d" % (addr, tx))
		if self.nodes[addr].isNormal(tx):
			self.bus.setTurnoutReverse(addr, tx)
			self.nodes[addr].setTurnoutReverse(tx)
		elif self.nodes[addr].isReversed(tx):
			self.bus.setTurnoutNormal(addr, tx)
			self.nodes[addr].setTurnoutNormal(tx)
		else:
			logging.error("Turnout cannot be toggled, not in normal or reversed state")
			return
			
		if self.createSocketServer:
			r = "{\"servos\": { \"address\": %d, \"delta\": true, \"count\": 1, \"values\":[" % addr 
			r += "[ %d, %d ]]}}" % (tx, self.nodes[addr].getTurnoutCurrent(tx))
			self.socketServer.sendToAll(r)
		
	def setOutputOn(self, addr, ox):
		logging.info("  Output %d:%d ON" % (addr, ox))
		self.bus.setOutputOn(addr, ox)
		self.nodes[addr].setOutputOn(ox)
		if self.createSocketServer:
			r = "{\"outputs\": {\"address\": %d, \"delta\": true, \"count\": 1, \"values\": [[%d, true]]}}" % (addr, ox)
			self.socketServer.sendToAll(r.encode())
		
	def setOutputPulse(self, addr, ox, pl):
		logging.info("  Output %d:%d PULSE %d" % (addr, ox, pl))
		self.bus.setOutputPulse(addr, ox, pl)
		self.nodes[addr].setOutputOff(ox) # after pulse, the output will be off, so record as off
		if self.createSocketServer:
			s = "{\"pulse\":{\"address\": %d, \"index\": %d, \"length\": %d}}" % (addr, ox, pl)
			self.socketServer.sendToAll(s.encode())
		
	def setOutputOff(self, addr, ox):
		logging.info("  Output %d:%d OFF" % (addr, ox))
		self.bus.setOutputOff(addr, ox)
		self.nodes[addr].setOutputOff(ox)
		if self.createSocketServer:
			r = "{\"outputs\": {\"address\": %d, \"delta\": true, \"count\": 1, \"values\": [[%d, false]]}}" % (addr, ox)
			self.socketServer.sendToAll(r.encode())

	def setAngle(self, addr, sx, ang):
		logging.info("  Servo %d:%d to angle %d" % (addr, sx, ang))
		self.bus.setAngle(addr, sx, ang)
		self.nodes[addr].setServoAngle(sx, ang)
		if self.createSocketServer:
			r = "{\"servos\": { \"address\": %d, \"delta\": true, \"count\": 1, \"values\":[" % addr 
			r += "[ %d, %d ]]}}" % (sx, self.nodes[addr].getTurnoutCurrent(sx))
			self.socketServer.sendToAll(r)

	def setTurnoutLimits(self, addr, tx, norm, rev, ini):		
		self.bus.setTurnoutLimits(addr, tx, norm, rev, ini)
		self.nodes[addr].setTurnoutLimits(tx, norm, rev, ini)
		if self.createSocketServer:
			r = "{\"servos\": { \"address\": %d, \"delta\": true, \"limits\": true, \"count\": 1, \"values\":[" % addr 
			r += "[ %d, %d, %d, %d ]]}}" % (tx, norm, rev, ini)
			self.socketServer.sendToAll(r)
	
	def setConfig(self, addr, naddr, inputs, outputs, servos):
		self.bus.setConfig(addr, naddr, inputs, outputs, servos)

	def outputRcvd(self, addr, vals):
		self.errors[addr] = 0
		rpt = "Output report for addr %d" % addr
		for i in range(len(vals)):
			self.nodes[addr].setOutput(i, vals[i]==1)
			rpt += "    %2d: %s" % (i, vals[i]==1)
			if (i+1) % 4 == 0:
				rpt += "\n"
		logging.info(rpt)
		if self.createSocketServer:
			s = self.outputsReport(addr)
			self.socketServer.sendToAll(s)
			
	def turnoutRcvd(self, addr, vals):
		self.errors[addr] = 0
		rpt = "Turnout report for address %d: (norm, rev, ini, cur)" % addr
		for i in range(len(vals)):
			v = vals[i]
			self.nodes[addr].setServoValues(i, v[0], v[1], v[2], v[3])
			rpt += "    %2d: %3d/%3d/%3d/%3d" % (i, v[0], v[1], v[2], v[3])
			if (i+1) % 4 == 0:
				rpt += "\n"
		logging.info(rpt)
		if self.createSocketServer:
			s = self.servosReport(addr)
			self.socketServer.sendToAll(s.encode())
			
	def msgRcvd(self, addr, cmd, msg):
		if cmd == ERRORRESPONSE:
			logging.error("Error from node at address %d: %s" % (addr, msg))
			self.errors[addr] += 1

		elif cmd == WARNINGRESPONSE:
			logging.warning("Warning from node at address %d: %s" % (addr, msg))
			#self.errors[addr] += 1

		else:
			s = "Unknown message received from address %d %02x: " % (addr, ord(cmd))   
			for c in msg:
				s += "%02x " % ord(c)
			logging.error(s)	
			self.errors[addr] += 1
			
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
				
				if addr not in self.nodes:
					self.HttpRespQ.put((400, b'unknown node address'))
					continue
				
				if verb == "init":
					self.startNode(addr)
					self.HttpRespQ.put((200, b'command accepted'))
					continue
				
				if not self.nodes[addr].isInitialized():
					msg = "communications with node %d has not been established" % addr
					self.HttpRespQ.put((400, msg.encode()))
					continue
				
				outp  = self.nodes[addr].getNOutputs()
				servo = self.nodes[addr].getNServos()
			else:
				addr = None

			if verb in ["reverse", "normal", "toggle"]:
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

				if tx < 0 or tx >= (servo):
					self.HttpRespQ.put((400, b'turnout index out of range'))
					continue

				if verb == "reverse":
					self.setTurnoutReverse(addr, tx)
				elif verb == "normal":
					self.setTurnoutNormal(addr, tx)
				else: # verb == toggle
					self.setTurnoutToggle(addr, tx)
					
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

				if sx < 0 or sx >= (servo):
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

				if ox < 0 or ox >= (outp):
					self.HttpRespQ.put((400, b'output index out of range'))
					continue

				if verb == "outoff":
					self.setOutputOff(addr, ox)
				else:
					self.setOutputOn(addr, ox)
				self.HttpRespQ.put((200, b'command performed'))

			elif verb == "pulse":
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

				if ox < 0 or ox >= (outp):
					self.HttpRespQ.put((400, b'output index out of range'))
					continue

				try:
					pl = int(cmd["length"][0])
				except KeyError:
					pl = 1 # default to a single cycle

				except ValueError:
					self.HttpRespQ.put((400, b'invalid value for pulse length'))
					continue
				except:
					self.HttpRespQ.put((400, b'unexpected error retrieving pulse length'))
					continue

				if pl < 0 or pl > 255:
					self.HttpRespQ.put((400, b'pulse length out of range'))
					continue

				if ox < 0 or ox >= (outp):
					self.HttpRespQ.put((400, b'output index out of range'))
					continue

				self.setOutputPulse(addr, ox, pl)
				self.HttpRespQ.put((200, b'command performed'))

			elif verb in ["inputs", "outputs", "turnouts", "servos", "getconfig"]:
				if verb == "inputs":
					resp = self.inputsReport(addr)
				elif verb == "outputs":
					resp = self.outputsReport(addr)
				elif verb in [ "turnouts", "servos" ]:
					resp = self.servosReport(addr)
				else: # verb == "getconfig"
					resp = str(self.nodes[addr])
					
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

				if tx < 0 or tx >= (servo):
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

				self.setConfig(addr, naddr, inputs, outputs, servos)
				self.HttpRespQ.put((200, b'command performed'))

			elif verb == "noderpt":
				report = self.nodesReport()
				self.HttpRespQ.put((200, report.encode()))

			elif verb == "store":
				self.bus.store(addr)
				
				self.HttpRespQ.put((200, b'command accepted'))

			elif verb == "quit":
				self.HttpRespQ.put((200, b'command accepted'))
				self.serving = False
				
			else:
				self.HttpRespQ.put((400, b'bad request'))
				
	def nodesReport(self):
		rpt  = "{\"nodes\": ["
		first = True
		for n in self.nodes:
			if not first:
				rpt += ", "
				
			first = False
			nd = self.nodes[n]
			rpt += str(nd)
		rpt += "]}"
		return rpt				
				
	def inputsReport(self, addr):
		inp = self.nodes[addr].getInputs()
		nin = self.nodes[addr].getNInputs()
		rpt = "{\"inputs\":{\"address\":%d,\"count\":%d,\"values\":[" % (addr, nin)
		inpStr = []
		for i in inp:
			inpStr.append("true" if i else "false")
		
		rpt += ", ".join(inpStr) + "]}}"
		return rpt

	def outputsReport(self, addr):
		outp = self.nodes[addr].getOutputs()
		nout= self.nodes[addr].getNOutputs()
		rpt = "{\"outputs\":{\"address\":%d,\"count\":%d,\"values\":[" % (addr, nout)
		outpStr = []
		for i in outp:
			outpStr.append("true" if i else "false")
		
		rpt += ", ".join(outpStr) + "]}}"
		return rpt

	def servosReport(self, addr):
		sv = self.nodes[addr].getServos()
		nsv= self.nodes[addr].getNServos()
		rpt = "{\"servos\":{\"address\":%d,\"count\":%d,\"values\":[" % (addr, nsv)
		svStr = []
		for i in sv:
			svStr.append(str(i))
		
		rpt += ", ".join(svStr) + "]}}"
		return rpt

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
		try:
			while not ticker.wait(interval) and self.serving:
				if self.serving:
					self.process()

		except KeyboardInterrupt:
			logging.info("Keyboard Interrupt - exiting...")
			print("Keyboard Interrupt - exiting...")

		ticker = None
		logging.info("Stopping HTTP Server...")
		self.stopHttpServer()
		
		if self.createSocketServer:	
			logging.info("Stopping socket server...")
			self.socketServer.kill()

		logging.info("disconnecting nodes...")
		self.disconnectNodes()

		logging.info("exiting...")

server = NodeServerMain("nodecfg.json")
server.serve_forever(0.25)

