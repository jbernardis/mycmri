#!/usr/bin/env python3

from bus import Bus
from httpserver import JMRIHTTPServer
from sktserver import SktServer
from triggertable import TriggerTable
from nodetypes import ERRORRESPONSE

import json
import queue
import threading

class JMRIMain:
	def __init__(self, cfgfn):
		self.cfgfn = cfgfn
		with open(cfgfn, "r") as fp:
			self.cfg = json.load(fp)

		print(json.dumps(self.cfg, sort_keys=True, indent=4))
		
		self.inputMaps = {}
		self.outputMaps = {}
		self.turnoutMaps = {}
		self.nodeCfg = {}
		self.createSocketServer = True
		towers = []
		if "nodes" not in self.cfg:
			print("Configuration file does not have any nodes defined")
			exit(1)

		if "ip" not in self.cfg:
			print("Configuration file does not specify an ip address for http server")
			exit(1)

		if "httpport" not in self.cfg:
			print("Configuration file does not specify an port for http server")
			exit(1)

		if "socketport" not in self.cfg:
			print("Configuration file does not define socket port. No server will be created.")
			self.createSocketServer = False

		if "tty" not in self.cfg:
			print("Configuration file does not specify a tty device for rs485 connection")
			exit(1)

		if "baud" not in self.cfg:
			print("Configuration file does not specify baud rate for rs485 bus")
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
		self.bus.connect(tty, baud)
		
		for n in self.cfg["nodes"]:
			try:
				print("Configuring bus: %s" % n["name"])
			except KeyError:
				print("Node name not specified")
				exit(1)

			try:
				ad = n["address"]
			except KeyError:
				print("Node %d does not specify an address" % n["name"])
				exit(1)
				
			if ad <= 0:
				print("Invalid node address - must be > 0")
				exit(1)
				

			try:
				inp = n["inputs"]
				outp = n["outputs"]
				servo = n["servos"]
				nm = n["name"]
			except KeyError:
				print("Node %s missing parameters - inputs, outputs, servos, name all required")
				exit(1)

			if ad in self.nodeCfg:
				print("Node %d is already defined - skipping" % ad)
			else:
				self.nodeCfg[ad] = (nm, inp, outp, servo)
				towers.append([ad, inp])
			
		self.bus.start([a[0] for a in towers])
		for ad in self.nodeCfg:
			self.bus.getIdentity(ad)
				
		self.triggerTable = TriggerTable(towers)
			
		self.startHttpServer(self.cfg["ip"], self.cfg["httpport"])
		if self.createSocketServer:
			self.socketServer = SktServer(self.cfg["ip"], self.cfg["socketport"])
			self.socketServer.start()
		
	def process(self):
		self.HTTPProcess()
		self.bus.process()
		
	def identityRcvd(self, addr, inp, outp, servo):
		msg = "Configuration received:\n  Addr: %d" % addr
		msg += "  Inputs: %d - %d channels\n" % (inp, inp*8)
		msg += "  Outputs: %d - %d channels\n" % (outp, outp*8)
		msg += "  Servos: %d - %d channels\n" % (servo, servo*16)	
		print(msg)

		# things to do the first time through		
		if not addr in self.inputMaps:
			self.inputMaps[addr] = [True] * (inp*8)		
			self.outputMaps[addr] = [0] * (outp*8)
			self.turnoutMaps[addr] = [[0, 0, 0, 0]] * (servo*16)
			
			nm = self.nodeCfg[addr][0]
			self.nodeCfg[addr] = (nm, inp, outp, servo)
			self.bus.setPoll(addr, True)
			self.bus.getCurrentInput(addr)
			self.bus.getCurrentOutput(addr)
			self.bus.getTurnouts(addr)

	def inputRcvd(self, addr, vals, delta):
		imap = self.inputMaps[addr]
		
		s = json.dumps({"addr": addr, "values": vals, "delta": delta})
		if self.createSocketServer:
			self.socketServer.sendToAll(s.encode())
		
		for inp, val in vals:
			imap[inp] = val == 1

		if not delta:
			print("Current input report for addr %d" % addr)
			
			i = 0
			for inp, val in vals:
				print("    %2d: %d" % (inp, val), end="")
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
				print("    %2d: %d" % (inp, val), end="")
				i += 1
				if i % 4 == 0:
					print("")
			print("")
				
			for inp, val in vals:
				print("check for trigger %d:%d" % (addr, inp))
				actions = self.triggerTable.checkInputTrigger(addr, inp)
				
				if len(actions) == 0:
					print("No actions triggered")
				else:
					print("Triggered actions (%d):" % len(actions))
					for a in actions:
						self.performAction(a[0], a[1], a[2:])
					print("")

	def performAction(self, verb, addr, parm):
		if addr not in self.nodeCfg:
			print("  %s action references unknown node address: %d" % (verb, addr))
			return

		if verb == "reverse":
			self.setTurnoutReverse(addr, parm[0])

		elif verb == "normal":
			self.setTurnoutNormal(addr, parm[0])
			
		elif verb == "outon":
			self.setOutputOn(addr, parm[0])
			
		elif verb == "outoff":
			self.setOutputOff(addr, parm[0])
			
		elif verb == "angle":
			self.bus.setAngle(addr, parm[0], parm[1])
			
		else:
			print("Unknown action verb: \"%s\".  Skipping action..." % verb)
			
	def setTurnoutNormal(self, addr, tx):
		print("  Normal turnout %d:%d" % (addr, tx))
		self.bus.setTurnoutNormal(addr, tx)
		self.turnoutMaps[addr][tx][3] = self.turnoutMaps[addr][tx][0]

	def setTurnoutReverse(self, addr, tx):
		print("  Reverse turnout %d:%d" % (addr, tx))
		self.bus.setTurnoutReverse(addr, tx)
		self.turnoutMaps[addr][tx][3] = self.turnoutMaps[addr][tx][1]
		
	def setOutputOn(self, addr, ox):
		print("  Output %d:%d ON" % (addr, ox))
		self.bus.setOutputOn(addr, ox)
		self.outputMaps[addr][ox] = 1
		
	def setOutputOff(self, addr, ox):
		print("  Output %d:%d OFF" % (addr, ox))
		self.bus.setOutputOff(addr, ox)
		self.outputMaps[addr][ox] = 0

	def setAngle(self, addr, sx, ang):
		print("  Servo %d:%d to angle %d" % (addr, sx, ang))
		self.bus.setAngle(addr, sx, ang)
		self.turnoutMaps[addr][sx][3] = ang

	def setTurnoutLimits(self, addr, tx, norm, rev, ini):		
		self.bus.setTurnoutLimits(addr, tx, norm, rev, ini)
		self.turnoutMaps[addr][tx][0] = norm
		self.turnoutMaps[addr][tx][1] = rev
		self.turnoutMaps[addr][tx][2] = ini
		
	def setConfig(self, addr, naddr, inputs, outputs, servos):
		self.bus.setConfig(addr, naddr, inputs, outputs, servos)


	def outputRcvd(self, addr, vals):
		print("Output report for addr %d" % addr)
		omap = self.outputMaps[addr]
		for i in range(len(vals)):
			omap[i] = vals[i]
			print("    %2d: %d" % (i, vals[i]), end="")
			if (i+1) % 4 == 0:
				print("")
		print("")
			
	def turnoutRcvd(self, addr, vals):
		print("Turnout report for address %d: (norm, rev, ini, cur)" % addr)
		tmap= self.turnoutMaps[addr]
		for i in range(len(vals)):
			v = vals[i]
			tmap[i] = v
			print("    %2d: %3d/%3d/%3d/%3d" % (i, v[0], v[1], v[2], v[3]), end="")
			if (i+1) % 4 == 0:
				print("")
		print("")

	def msgRcvd(self, addr, cmd, msg):
		if cmd == ERRORRESPONSE:
			print("Error from node at address %d: %s" % (addr, msg))
		else:
			s = "Unknown message received from address %d %02x: " % (addr, ord(cmd))   
			for c in msg:
				s += "%02x " % ord(c)
			print(s)	
			
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

			if not verb in ["quit", "towers"]:
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

			elif verb in ["inputs", "outputs", "turnouts", "config"]:
				if verb == "inputs":
					resp = str(self.inputMaps[addr])
				elif verb == "outputs":
					resp = str(self.outputMaps[addr])
				elif verb == "turnouts":
					resp = str(self.turnoutMaps[addr])
				else: # verb == "config"
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

			elif verb == "config":
				try:
					naddr = int(cmd["addr"][0])
				except KeyError:
					self.HttpRespQ.put((400, b'missing address'))
					continue
				except ValueError:
					self.HttpRespQ.put((400, b'invalid value for node address'))
					continue
				except:
					self.HttpRespQ.put((400, b'unexpected error retrieving address'))
					continue

				if naddr < 1 or naddr > 99:
					self.HttpRespQ.put((400, b'address out of range'))
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

			elif verb == "towers":
				result = "{"
				first = True
				for n in self.nodeCfg:
					if not first:
						result += ", "
					first = False
					cfg = self.nodeCfg[n]
					result += "'%s': {'addr': %d, 'input': %d, 'output': %d, 'servo': %d} " % (cfg[0], n, cfg[1], cfg[2], cfg[3])
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
		print("Starting HTTP server at address: %s:%d" % (ip, port))
		self.HttpCmdQ = queue.Queue(0)
		self.HttpRespQ = queue.Queue(0)
		self.serving = True
		self.jmriserver = JMRIHTTPServer(ip, port, self.HttpCmdQ, self.HttpRespQ)

	def disconnectNodes(self):
			try:
				self.bus.stop()
				self.bus.disconnect()

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
		
		print("Stopping socket server...")
		self.socketServer.kill()

		print("disconnecting nodes...")
		self.disconnectNodes()

		print("exiting...")

jmri = JMRIMain("jmri.json")
jmri.serve_forever(0.25)

