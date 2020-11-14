'''
Created on Aug 11, 2020

@author: jeff
'''
import requests
import logging

class Server(object):
	def __init__(self):
		self.ipAddr = None
	
	def setServerAddress(self, ip, port):
		logging.info("setting server address to %s:%s" % (ip, port))
		self.ipAddr = "http://%s:%s" % (ip, port)
	
	def setTurnoutNormal(self, addr, tx):
		r = requests.get(self.ipAddr, params={"cmd": "normal", "addr": addr, "index": tx})
		return r.status_code, r.text
	
	def setTurnoutReverse(self, addr, tx):
		r = requests.get(self.ipAddr, params={"cmd": "reverse", "addr": addr, "index": tx})
		return r.status_code, r.text
	
	def setTurnoutToggle(self, addr, tx):
		r = requests.get(self.ipAddr, params={"cmd": "toggle", "addr": addr, "index": tx})
		return r.status_code, r.text
	
	def setServoAngle(self, addr, sx, ang):
		r = requests.get(self.ipAddr, params={"cmd": "angle", "addr": addr, "index": sx, "angle": ang})
		return r.status_code, r.text
	
	def setlimits(self, addr, tx, norm, rev, ini):
		r = requests.get(self.ipAddr, params={"cmd": "setlimits", "addr": addr, "index": tx, \
											"normal": norm, "reverse": rev, "initial": ini})
		return r.status_code, r.text
	
	def setOutputOn(self, addr, ox):
		r = requests.get(self.ipAddr, params={"cmd": "outon", "addr": addr, "index": ox})
		return r.status_code, r.text
	
	def setOutputOff(self, addr, ox):
		r = requests.get(self.ipAddr, params={"cmd": "outoff", "addr": addr, "index": ox})
		return r.status_code, r.text
		
	def getInputs(self, addr):
		r = requests.get(self.ipAddr, params={"cmd": "inputs", "addr": addr})
		return r.status_code, r.text
		
	def getOutputs(self, addr):
		r = requests.get(self.ipAddr, params={"cmd": "outputs", "addr": addr})
		return r.status_code, r.text
		
	def getTurnouts(self, addr):
		r = requests.get(self.ipAddr, params={"cmd": "turnouts", "addr": addr})
		return r.status_code, r.text
	
	def setFlag(self, addr, fx):
		r = requests.get(self.ipAddr, params={"cmd": "setflag", "addr": addr, "index": fx})
		return r.status_code, r.text
	
	def clearFlag(self, addr, fx):
		r = requests.get(self.ipAddr, params={"cmd": "clearflag", "addr": addr, "index": fx})
		return r.status_code, r.text
		
	def getFlags(self, addr):
		r = requests.get(self.ipAddr, params={"cmd": "flags", "addr": addr})
		return r.status_code, r.text
	
	def setRegister(self, addr, rx, value):
		r = requests.get(self.ipAddr, params={"cmd": "setregister", "addr": addr, "index": rx, "value": value})
		return r.status_code, r.text
		
	def getRegisters(self, addr):
		r = requests.get(self.ipAddr, params={"cmd": "registers", "addr": addr})
		return r.status_code, r.text
		
	def getConfig(self, addr):
		r = requests.get(self.ipAddr, params={"cmd": "getconfig", "addr": addr})
		return r.status_code, r.text
		
	def setConfig(self, addr, naddr, inputs, outputs, servos):
		r = requests.get(self.ipAddr, params={"cmd": "setconfig", "addr": addr, "naddr": naddr, "inputs": inputs, "outputs": outputs, "servos": servos})
		return r.status_code, r.text
		
	def nodeRefresh(self, addr):
		r = requests.get(self.ipAddr, params={"cmd": "refresh", "addr": addr})
		return r.status_code, r.text
		
	def nodeStore(self, addr):
		r = requests.get(self.ipAddr, params={"cmd": "store", "addr": addr})
		return r.status_code, r.text
		
	def nodeInit(self, addr):
		r = requests.get(self.ipAddr, params={"cmd": "init", "addr": addr})
		return r.status_code, r.text
	
	def getNodeRpt(self):
		r = requests.get(self.ipAddr, params={"cmd": "noderpt"})
		return r.status_code, r.text
	
	def quit(self):
		r = requests.get(self.ipAddr, params={"cmd": "quit"})
		return r.status_code, r.text

		