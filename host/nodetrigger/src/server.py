'''
Created on Aug 11, 2020

@author: jeff
'''
import requests

class Server(object):
	def __init__(self):
		self.ipAddr = None
	
	def setServerAddress(self, ip, port):
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
	
	def setOutputOn(self, addr, ox):
		r = requests.get(self.ipAddr+"/outon", params={"addr": addr, "index": ox})
		return r.status_code, r.text
	
	def setOutputOff(self, addr, ox):
		r = requests.get(self.ipAddr+"/outoff", params={"addr": addr, "index": ox})
		return r.status_code, r.text
	
	def pulseOutput(self, addr, ox, pl):
		r = requests.get(self.ipAddr+"/pulse", params={"addr": addr, "index": ox, "length": pl})
		return r.status_code, r.text
		
