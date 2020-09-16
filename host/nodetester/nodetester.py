#!/usr/bin/env python3

#import wx
import wx.lib.newevent
import json
from images import Images 
from server import Server
from listener import Listener
from inputsdlg import InputsDlg
from outputsdlg import OutputsDlg
from servosdlg import ServosDlg

import os

SVRLABELW = 80
CFGLABELW = 80

iperckt = 8
operckt = 8
tperckt = 16

(DeliveryEvent, EVT_DELIVERY) = wx.lib.newevent.NewEvent()   # @UndefinedVariable
(DisconnectEvent, EVT_DISCONNECT) = wx.lib.newevent.NewEvent()   # @UndefinedVariable
	
class NodeTester(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, wx.ID_ANY, "Node Tester", size=(500, 500))
		self.SetBackgroundColour(wx.Colour(255, 255, 255))
		self.Bind(wx.EVT_CLOSE, self.onClose)
		
		self.images = Images("images")
		self.ipAddress = "192.168.1.210"
		self.httpPort = "8000"
		self.socketPort = "8001"
		self.server = Server()
		self.listener = None
		
		self.inputs = 1
		self.outputs = 1
		self.servos = 1
		self.inputsMap = []
		self.outputsMap = []
		self.servosMap = []
		self.subscribed = False
		self.currentDisplayedAddr = None

		
		self.timer = wx.Timer(self)
		self.clearTimer = None
		
		sz = wx.BoxSizer(wx.VERTICAL)
		sz.AddSpacer(2)
		self.dlgInputs = None
		self.dlgOutputs = None
		self.dlgServos = None
		
		boxSvr = wx.StaticBox(self, wx.ID_ANY, " Server ")
		topBorder, botBorder = boxSvr.GetBordersForSizer()
		if os.name != 'nt':
			botBorder += 30
			
		bsizer = wx.BoxSizer(wx.VERTICAL)
		bsizer.AddSpacer(topBorder)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(10)
		hsizer.Add(wx.StaticText(boxSvr, wx.ID_ANY, "IP Address:", size=(SVRLABELW, -1)))
		self.teIpAddr = wx.TextCtrl(boxSvr, wx.ID_ANY, self.ipAddress, size=(125, -1))
		hsizer.Add(self.teIpAddr)
		hsizer.AddSpacer(10)
		bsizer.Add(hsizer)
		
		bsizer.AddSpacer(5)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(10)
		hsizer.Add(wx.StaticText(boxSvr, wx.ID_ANY, "HTTP Port:", size=(SVRLABELW, -1)))
		self.teHPort = wx.TextCtrl(boxSvr, wx.ID_ANY, self.httpPort, size=(125, -1))
		hsizer.Add(self.teHPort)
		hsizer.AddSpacer(10)
		bsizer.Add(hsizer)
		
		bsizer.AddSpacer(5)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(10)
		hsizer.Add(wx.StaticText(boxSvr, wx.ID_ANY, "Socket Port:", size=(SVRLABELW, -1)))
		self.teSPort = wx.TextCtrl(boxSvr, wx.ID_ANY, self.socketPort, size=(125, -1))
		hsizer.Add(self.teSPort)
		hsizer.AddSpacer(10)
		self.bSubscribe = wx.Button(boxSvr, wx.ID_ANY, "Subscribe")
		self.Bind(wx.EVT_BUTTON, self.onSubscribe, self.bSubscribe)
		hsizer.Add(self.bSubscribe)
		hsizer.AddSpacer(10)
		bsizer.Add(hsizer)
		
		bsizer.AddSpacer(botBorder)

		boxSvr.SetSizer(bsizer)	
		sz.Add(boxSvr, 0, wx.EXPAND|wx.ALL, 5)	
		sz.AddSpacer(10)
			
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(10)
		hsizer.Add(wx.StaticText(self, wx.ID_ANY, "Node Address:"))
		hsizer.AddSpacer(10)
		self.scAddress = wx.SpinCtrl(self, wx.ID_ANY, "", (30, 50))
		self.scAddress.SetRange(1,100)
		self.scAddress.SetValue(1)
		hsizer.Add(self.scAddress)
		hsizer.AddSpacer(10)
		self.bGetConfig = wx.Button(self, wx.ID_ANY, "Get Config")
		self.Bind(wx.EVT_BUTTON, self.onGetConfig, self.bGetConfig)
		hsizer.Add(self.bGetConfig)
		hsizer.AddSpacer(10)
		self.bRefresh = wx.Button(self, wx.ID_ANY, "Refresh")
		self.Bind(wx.EVT_BUTTON, self.onRefresh, self.bRefresh)
		hsizer.Add(self.bRefresh)

		sz.Add(hsizer)
		
		sz.AddSpacer(10)
				
		boxCfg = wx.StaticBox(self, wx.ID_ANY, " Node Config ")
		topBorder, botBorder = boxCfg.GetBordersForSizer()
		if os.name != 'nt':
			botBorder += 30
		bsizer = wx.BoxSizer(wx.VERTICAL)
		bsizer.AddSpacer(topBorder)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(10)
		hsizer.Add(wx.StaticText(boxCfg, wx.ID_ANY, "Inputs:", size=(CFGLABELW, -1)))
		self.stInputs = wx.StaticText(boxCfg, wx.ID_ANY, "")
		hsizer.Add(self.stInputs)
		hsizer.AddSpacer(10)
		bsizer.Add(hsizer)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(10)
		hsizer.Add(wx.StaticText(boxCfg, wx.ID_ANY, "Ouputs:", size=(CFGLABELW, -1)))
		self.stOutputs = wx.StaticText(boxCfg, wx.ID_ANY, "")
		hsizer.Add(self.stOutputs)
		hsizer.AddSpacer(10)
		bsizer.Add(hsizer)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(10)
		hsizer.Add(wx.StaticText(boxCfg, wx.ID_ANY, "Servos:", size=(CFGLABELW, -1)))
		self.stServos = wx.StaticText(boxCfg, wx.ID_ANY, "")
		hsizer.Add(self.stServos)
		hsizer.AddSpacer(10)
		bsizer.Add(hsizer)
		bsizer.AddSpacer(botBorder)
		
		self.setConfigValues(1, 1, 1)

		boxCfg.SetSizer(bsizer)	
		sz.Add(boxCfg, 0, wx.EXPAND|wx.ALL, 5)	
		
		sz.AddSpacer(10)
		
		bsz = wx.BoxSizer(wx.HORIZONTAL)
		
		self.bInputs = wx.Button(self, wx.ID_ANY, "Inputs")
		bsz.Add(self.bInputs)
		self.Bind(wx.EVT_BUTTON, self.onBInputs, self.bInputs)
		
		bsz.AddSpacer(5)
		
		self.bOutputs = wx.Button(self, wx.ID_ANY, "Outputs")
		bsz.Add(self.bOutputs)
		self.Bind(wx.EVT_BUTTON, self.onBOutputs, self.bOutputs)
		
		bsz.AddSpacer(5)
		
		self.bServos = wx.Button(self, wx.ID_ANY, "Servos")
		bsz.Add(self.bServos)
		self.Bind(wx.EVT_BUTTON, self.onBServos, self.bServos)
		
		sz.Add(bsz)

		sz.AddSpacer(20)
		
		mainsz = wx.BoxSizer(wx.HORIZONTAL)
		mainsz.AddSpacer(20)
		mainsz.Add(sz)
		mainsz.AddSpacer(20)
		
		wsz = wx.BoxSizer(wx.VERTICAL)
		wsz.Add(mainsz)
		self.statusBar = wx.StatusBar(self, wx.ID_ANY, style=wx.STB_ELLIPSIZE_END)
		self.statusBar.SetStatusStyles([wx.SB_FLAT])
		wsz.Add(self.statusBar, 0, wx.EXPAND|wx.RIGHT)
		
		self.SetSizer(wsz)
		
		self.Layout()
		self.Fit()
		self.Show()
		
		self.timer.Start(1000)
		self.Bind(wx.EVT_TIMER, self.onTimer)
		self.Bind(EVT_DELIVERY, self.onDeliveryEvent)
		self.Bind(EVT_DISCONNECT, self.onDisconnectEvent)
		
	def onBInputs(self, _):
		addr = self.scAddress.GetValue()
		if addr != self.currentDisplayedAddr:
			self.setStatusText("Retrieve configuration first")
		else:
			self.openInputsDlg()
		
	def openInputsDlg(self):
		if len(self.inputsMap) == 0:
			self.setStatusText("No inputs information available")
			return

		pos = None		
		if self.dlgInputs is not None:
			try:
				pos = self.dlgInputs.GetScreenPosition()
				self.dlgInputs.Destroy()
			except:
				pos = None
			
		self.dlgInputs =  InputsDlg(self, self.inputsMap, self.inputs, self.scAddress.GetValue())
		if pos is not None:
			self.dlgInputs.SetPosition(pos)
		self.dlgInputs.Show()
		
	def dlgInputsExit(self):
		self.dlgInputs = None
		
	def onBOutputs(self, _):
		addr = self.scAddress.GetValue()
		if addr != self.currentDisplayedAddr:
			self.setStatusText("Retrieve configuration first")
		else:
			self.openOutputsDlg()
		
	def openOutputsDlg(self):
		if len(self.outputsMap) == 0:
			self.setStatusText("No outputs information available")
			return

		pos = None		
		if self.dlgOutputs is not None:
			try:
				pos = self.dlgOutputs.GetScreenPosition()
				self.dlgOutputs.Destroy()
			except:
				pos = None
			
		self.dlgOutputs =  OutputsDlg(self, self.outputsMap, self.outputs, self.scAddress.GetValue())
		if pos is not None:
			self.dlgOutputs.SetPosition(pos)
		self.dlgOutputs.Show()
		
	def dlgOutputsExit(self):
		self.dlgOutputs = None
		
	def onBServos(self, _):
		addr = self.scAddress.GetValue()
		if addr != self.currentDisplayedAddr:
			self.setStatusText("Retrieve configuration first")
		else:
			self.openServosDlg()
		
	def openServosDlg(self):
		if len(self.servosMap) == 0:
			self.setStatusText("No outputs information available")
			return

		pos = None		
		if self.dlgServos is not None:
			try:
				pos = self.dlgServos.GetScreenPosition()
				self.dlgServos.Destroy()
			except:
				pos = None
			
		self.dlgServos =  ServosDlg(self, self.servosMap, self.servos, self.scAddress.GetValue())
		if pos is not None:
			self.dlgServos.SetPosition(pos)
		self.dlgServos.Show()
		
	def dlgServosExit(self):
		self.dlgServos = None
		
	def throwTurnout(self, tx, normal):
		ip = self.teIpAddr.GetValue()
		pt = self.teHPort.GetValue()
		addr = self.scAddress.GetValue()
		self.server.setServerAddress(ip, pt)

		if normal:
			try:
				sc, data = self.server.setTurnoutNormal(addr, tx)
			except:
				self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
				return False
		else:
			try:
				sc, data = self.server.setTurnoutReverse(addr, tx)
			except:
				self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
				return False
			
		if sc < 400:
			try:
				if normal:
					self.servosMap[tx][3] = self.servosMap[tx][0]
				else:
					self.servosMap[tx][3] = self.servosMap[tx][1]
				self.setStatusText("Success")
				return True
			except:
				self.setStatusText("Unable to process return data: '%s'" % data)
				return False
		else:
			self.setStatusText("Unexpected HTTP return code: %d" % sc)
			return False
		
	def setServoAngle(self, sx, ang):
		ip = self.teIpAddr.GetValue()
		pt = self.teHPort.GetValue()
		addr = self.scAddress.GetValue()
		self.server.setServerAddress(ip, pt)
		try:
			sc, data = self.server.setServoAngle(addr, sx, ang)
		except:
			self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
			return False

		if sc < 400:
			try:
				self.servosMap[sx][3] = ang
				self.setStatusText("Success")
				return True
			except:
				self.setStatusText("Unable to process return data: '%s'" % data)
				return False
		else:
			self.setStatusText("Unexpected HTTP return code: %d" % sc)
			return False
		
	def setTurnoutLimits(self, tx, norm, rev, ini):
		ip = self.teIpAddr.GetValue()
		pt = self.teHPort.GetValue()
		addr = self.scAddress.GetValue()
		self.server.setServerAddress(ip, pt)
		try:
			sc, data = self.server.setlimits(addr, tx, norm, rev, ini)
		except:
			self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
			return False

		if sc < 400:
			try:
				self.servosMap[tx][0] = norm
				self.servosMap[tx][1] = rev
				self.servosMap[tx][2] = ini
				self.setStatusText("Success")
				return True
			except:
				self.setStatusText("Unable to process return data: '%s'" % data)
				return False
		else:
			self.setStatusText("Unexpected HTTP return code: %d" % sc)
			return False
		
	def swapTurnout(self, tx):
		ip = self.teIpAddr.GetValue()
		pt = self.teHPort.GetValue()
		addr = self.scAddress.GetValue()
		self.server.setServerAddress(ip, pt)
		sv = self.servosMap[tx]
		norm = sv[0]
		rev = sv[1]

		try:
			sc, data = self.server.setlimits(addr, tx, rev, norm, sv[2])
		except:
			self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
			return False
			
		if sc < 400:
			try:
				self.servosMap[tx][0] = rev
				self.servosMap[tx][1] = norm
				self.setStatusText("Success")
				return True
			except:
				self.setStatusText("Unable to process return data: '%s'" % data)
				return False
		else:
			self.setStatusText("Unexpected HTTP return code: %d" % sc)
			return False
		
	def getServosMap(self):
		return self.servosMap
			
	def setOutput(self, bn, newState):
		ip = self.teIpAddr.GetValue()
		pt = self.teHPort.GetValue()
		addr = self.scAddress.GetValue()
		self.server.setServerAddress(ip, pt)
		
		if newState:
			try:
				sc, data = self.server.setOutputOn(addr, bn)
			except:
				self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
				return False
		else:
			try:
				sc, data = self.server.setOutputOff(addr, bn)
			except:
				self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
				return False
		
		if sc < 400:
			try:
				self.outputsMap[bn] = newState
				self.setStatusText("Success")
				return True
			except:
				self.setStatusText("Unable to process return data: '%s'" % data)
				return False
		else:
			self.setStatusText("Unexpected HTTP return code: %d" % sc)
			return False
		
	def setConfigValues(self, i, o, s):
		self.inputs = i
		
		self.stInputs.SetLabel("%d (%d total)" % (i, i*iperckt))
		self.outputs = o
		self.stOutputs.SetLabel("%d (%d total)" % (o, o*operckt))
		self.servos = s
		self.stServos.SetLabel("%d (%d total)" % (s, s*tperckt))
		
	def onSubscribe(self, _):
		if self.subscribed:
			self.listener.kill()
			self.listener.join()
			self.listener = None
			self.subscribed = False
			self.bSubscribe.SetLabel("Subscribe")
		else:
			ip = self.teIpAddr.GetValue()
			pt = self.teSPort.GetValue()
			self.listener = Listener(self, ip, pt)
			self.listener.start()
			self.subscribed = True
			self.bSubscribe.SetLabel("Unsubscribe")
			
	def raiseDeliveryEvent(self, data):
		jdata = json.loads(data)
		evt = DeliveryEvent(data=jdata)
		wx.PostEvent(self, evt)
		
	def raiseDisconnectEvent(self):
		evt = DisconnectEvent()
		wx.PostEvent(self, evt)
	
	def onDisconnectEvent(self, _):
		self.listener = None
		self.subscribed = False
		self.bSubscribe.SetLabel("Subscribe")
		self.setStatusText("Server socket closed")
		
	def setStatusText(self, text):
		self.clearTimer = 10
		self.statusBar.SetStatusText(text)
		print(text)

	def onGetConfig(self, _):
		self.loadConfig()
		
	def onRefresh(self, _):
		ip = self.teIpAddr.GetValue()
		pt = self.teHPort.GetValue()
		addr = self.scAddress.GetValue()
		self.server.setServerAddress(ip, pt)
		
		try:
			sc, _ = self.server.nodeRefresh(addr)
				
		except:
			self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
			return
		
		if sc >= 400:
			self.setStatusText("Unexpected HTTP return code: %d" % sc)
			return False
			
		self.setStatusText("Refresh Success")
		self.loadConfig()
		
	def loadConfig(self):
		ip = self.teIpAddr.GetValue()
		pt = self.teHPort.GetValue()
		addr = self.scAddress.GetValue()
		self.currentDisplayedAddr = addr
		self.server.setServerAddress(ip, pt)
		try:
			sc, data = self.server.getConfig(addr)
		except:
			self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
			return 
		
		if sc < 400:
			try:
				d = eval(data)
				self.setConfigValues(d[1], d[2], d[3])
				self.setStatusText("Retrieve Node Config Success")
			except:
				self.setStatusText("Unable to process return data: '%s'" % data)
		else:
			self.setStatusText("Unexpected HTTP return code: %d" % sc)
			
		try:
			sc, data = self.server.getInputs(addr)
		except:
			self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
			return 
		
		if sc < 400:
			try:
				self.inputsMap = eval(data)
				self.openInputsDlg()
				self.setStatusText("Retrieve Inputs Success")
			except:
				self.inputsMap = []
				self.setStatusText("Unable to process return data: '%s'" % data)
		else:
			self.setStatusText("Unexpected HTTP return code: %d" % sc)
			
		try:
			sc, data = self.server.getOutputs(addr)
		except:
			self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
			return 
		
		if sc < 400:
			try:
				self.outputsMap = eval(data)
				self.openOutputsDlg()
				self.setStatusText("Retrieve Outputs Success")
			except:
				self.outputsMap = []
				self.setStatusText("Unable to process return data: '%s'" % data)
		else:
			self.setStatusText("Unexpected HTTP return code: %d" % sc)
			
		try:
			sc, data = self.server.getTurnouts(addr)
		except:
			self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
			return 
		
		if sc < 400:
			try:
				self.servosMap = eval(data)
				self.openServosDlg()
				self.setStatusText("Retrieve Turnouts Success")
			except:
				self.servosMap = []
				self.setStatusText("Unable to process return data: '%s'" % data)
		else:
			self.setStatusText("Unexpected HTTP return code: %d" % sc)
			
	def onDeliveryEvent(self, evt):
		msgType = evt.data["type"]
		if msgType == "input":
			iaddr = evt.data["addr"]
			
			if iaddr != self.currentDisplayedAddr:
				return 
			
			if evt.data["delta"]:
				vals = evt.data["values"]
				if len(vals) > 0:
					for inp, val in vals:
						self.inputsMap[inp] = val == 1
					if self.dlgInputs is not None:
						self.dlgInputs.update(self.inputsMap)
	
			else:
				vals = evt.data["values"]
				if len(vals) == len(self.inputsMap):
					self.inputsMap = [x == 1 for x in vals]
					if self.dlgInputs is not None:
						self.dlgInputs.update(self.inputsMap)
				else:
					self.setStatusText("Mismatch number of inputs")
					
		elif msgType == "output":
			print("output report rcvd")
			iaddr = evt.data["addr"]
			
			if iaddr != self.currentDisplayedAddr:
				return 
			
			vals = evt.data["values"]
			if len(vals) == len(self.outputsMap):
				self.outputsMap = [x for x in vals]
				if self.dlgOutputs is not None:
					self.dlgOutputs.update(self.outputsMap)
			else:
				self.setStatusText("Mismatch number of outputs")
			
		elif msgType == "turnout":
			print("turnout report rcvd")
			iaddr = evt.data["addr"]
			
			if iaddr != self.currentDisplayedAddr:
				return 
			
			vals = evt.data["values"]
			if len(vals) == len(self.servosMap):
				self.servosMap = [x for x in vals]
				if self.dlgServos is not None:
					self.dlgServos.update(self.servosMap)
			else:
				self.setStatusText("Mismatch number of turnouts/servos")
						
		else:
			print("Unknown report type (%s)" % msgType)
			
	def onMessageEvent(self, evt):
		self.setStatusText(evt.message)
			
	def onTimer(self, _):
		if self.clearTimer is None:
			return 
		
		self.clearTimer -= 1
		if self.clearTimer <= 0:
			self.statusBar.SetStatusText("")

		
	def onClose(self, _):
		if self.listener is not None:
			self.setStatusText("destroying listener thread")
			self.listener.kill()
			self.listener.join()

		print("exiting")			
		self.Destroy()

if __name__ == '__main__':
	app = wx.App()
	frame = NodeTester()
	frame.Show(True)
	app.MainLoop()
