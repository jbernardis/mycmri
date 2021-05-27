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
		r = requests.get(self.ipAddr+"/normal", params={"addr": addr, "index": tx})
		return r.status_code, r.text
	
	def setTurnoutReverse(self, addr, tx):
		r = requests.get(self.ipAddr+"/reverse", params={"addr": addr, "index": tx})
		return r.status_code, r.text
	
	def setTurnoutToggle(self, addr, tx):
		r = requests.get(self.ipAddr+"/toggle", params={"addr": addr, "index": tx})
		return r.status_code, r.text
	
	def setServoAngle(self, addr, sx, ang):
		r = requests.get(self.ipAddr+"/angle", params={"addr": addr, "index": sx, "angle": ang})
		return r.status_code, r.text
	
	def setlimits(self, addr, tx, norm, rev, ini):
		r = requests.get(self.ipAddr+"/setlimits", params={"addr": addr, "index": tx, \
											"normal": norm, "reverse": rev, "initial": ini})
		return r.status_code, r.text
	
	def setOutputOn(self, addr, ox):
		r = requests.get(self.ipAddr+"/outon", params={"addr": addr, "index": ox})
		return r.status_code, r.text
	
	def setOutputOff(self, addr, ox):
		r = requests.get(self.ipAddr+"/outoff", params={"addr": addr, "index": ox})
		return r.status_code, r.text
		
	def getInputs(self, addr):
		r = requests.get(self.ipAddr+"/inputs", params={"addr": addr})
		return r.status_code, r.text
		
	def getOutputs(self, addr):
		r = requests.get(self.ipAddr+"/outputs", params={"addr": addr})
		return r.status_code, r.text
		
	def getTurnouts(self, addr):
		r = requests.get(self.ipAddr+"/turnouts", params={"addr": addr})
		return r.status_code, r.text
	
	def getConfig(self, addr):
		r = requests.get(self.ipAddr+"/getconfig", params={"addr": addr})
		return r.status_code, r.text
		
	def setConfig(self, addr, naddr, inputs, outputs, servos):
		r = requests.get(self.ipAddr+"/setconfig", params={"addr": addr, "naddr": naddr, "inputs": inputs, "outputs": outputs, "servos": servos})
		return r.status_code, r.text
		
	def nodeRefresh(self, addr):
		r = requests.get(self.ipAddr+"/refresh", params={"addr": addr})
		return r.status_code, r.text
		
	def nodeStore(self, addr):
		r = requests.get(self.ipAddr+"/store", params={"addr": addr})
		return r.status_code, r.text
		
	def nodeInit(self, addr):
		r = requests.get(self.ipAddr+"/init", params={"addr": addr})
		return r.status_code, r.text
	
	def getNodeRpt(self):
		r = requests.get(self.ipAddr+"/noderpt")
		return r.status_code, r.text
	
	def quit(self):
		r = requests.get(self.ipAddr+"/quit")
		return r.status_code, r.text

		