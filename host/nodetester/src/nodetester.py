#!/usr/bin/env python3

#import wx
import wx.lib.newevent
import json
from images import Images 
from server import Server
from listener import Listener
from nodedlg import NodeDlg
from inputsdlg import InputsDlg
from outputsdlg import OutputsDlg
from servosdlg import ServosDlg
from nodeconfigdlg import NodeConfigDlg

import os
import queue

SVRLABELW = 80
CFGLABELW = 80

MENU_SERVER_NODES = 101
MENU_SERVER_SHUTDOWN = 109
MENU_NODE_CONFIG = 201
MENU_NODE_INIT = 202
MENU_WINDOW_INPUTS = 301
MENU_WINDOW_OUTPUTS = 302
MENU_WINDOW_SERVOS = 303

(DeliveryEvent, EVT_DELIVERY) = wx.lib.newevent.NewEvent()   # @UndefinedVariable
(DisconnectEvent, EVT_DISCONNECT) = wx.lib.newevent.NewEvent()   # @UndefinedVariable
	
class NodeTester(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, wx.ID_ANY, "Node Tester", size=(500, 500))
		self.SetBackgroundColour(wx.Colour(255, 255, 255))
		self.Bind(wx.EVT_CLOSE, self.onClose)
		
		self.CreateStatusBar()
		self.qStatus = queue.Queue()

		menuBar = wx.MenuBar()
		self.menuServer = wx.Menu()
		self.menuServer.Append(MENU_SERVER_NODES, "Nodes Report", "Get Nodes Report")
		self.menuServer.Append(MENU_SERVER_SHUTDOWN, "Shut down", "Shut down server")
		self.menuNode = wx.Menu()
		self.menuNode.Append(MENU_NODE_CONFIG, "Re-Config", "Modify current node configuration")
		self.menuNode.Append(MENU_NODE_INIT, "Init", "Reinit the node communicatione with the server")
		self.menuWindow = wx.Menu()
		self.menuWindow.Append(MENU_WINDOW_INPUTS, "Inputs")
		self.menuWindow.Append(MENU_WINDOW_OUTPUTS, "Outputs")
		self.menuWindow.Append(MENU_WINDOW_SERVOS, "Servos/Turnouts")
		
		menuBar.Append(self.menuServer, "Server")
		menuBar.Append(self.menuNode, "Node")
		menuBar.Append(self.menuWindow, "Window")
		
		self.Bind(wx.EVT_MENU, self.onMenuNodes, id=MENU_SERVER_NODES)		
		self.Bind(wx.EVT_MENU, self.onMenuShutdown, id=MENU_SERVER_SHUTDOWN)		
		self.Bind(wx.EVT_MENU, self.onMenuConfig, id=MENU_NODE_CONFIG)		
		self.Bind(wx.EVT_MENU, self.onMenuInit, id=MENU_NODE_INIT)		
		self.Bind(wx.EVT_MENU, self.onMenuInputs, id=MENU_WINDOW_INPUTS)		
		self.Bind(wx.EVT_MENU, self.onMenuOutputs, id=MENU_WINDOW_OUTPUTS)		
		self.Bind(wx.EVT_MENU, self.onMenuServos, id=MENU_WINDOW_SERVOS)	
		
		self.SetMenuBar(menuBar)
		
		self.images = Images("images")
		self.ipAddress = "192.168.1.142"
		self.httpPort = "8000"
		self.socketPort = "8001"
		self.server = Server()
		self.listener = None
		
		self.inputs = 1
		self.outputs = 1
		self.servos = 1
		self.flags = 0
		self.registers = 0
		self.inputsMap = []
		self.outputsMap = []
		self.servosMap = []
		self.subscribed = False
		self.currentNodeAddr = None

		
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
		self.Bind(wx.EVT_TEXT, self.onTeIpAddrChange, self.teIpAddr)
		self.teIpAddr.Bind(wx.EVT_KILL_FOCUS, self.onTeIpAddrLoseFocus)
		self.teIpAddr.Bind(wx.EVT_SET_FOCUS, self.onTeIpAddrSetFocus)
		hsizer.Add(self.teIpAddr)
		hsizer.AddSpacer(10)
		bsizer.Add(hsizer)
		
		bsizer.AddSpacer(5)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(10)
		hsizer.Add(wx.StaticText(boxSvr, wx.ID_ANY, "HTTP Port:", size=(SVRLABELW, -1)))
		self.teHPort = wx.TextCtrl(boxSvr, wx.ID_ANY, self.httpPort, size=(125, -1))
		self.Bind(wx.EVT_TEXT, self.onTeHPortChange, self.teHPort)
		self.teHPort.Bind(wx.EVT_KILL_FOCUS, self.onTeHPortLoseFocus)
		self.teHPort.Bind(wx.EVT_SET_FOCUS, self.onTeHPortSetFocus)
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
		self.bSubscribe.SetToolTip("Subscribe to receive asynchronous reports from the server")
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
		
		self.stAddr = wx.StaticText(self, wx.ID_ANY, "   ")
		hsizer.Add(self.stAddr)
		hsizer.AddSpacer(20)
		
		self.bGetAddr = wx.Button(self, wx.ID_ANY, "...", size=(30, -1))
		self.bGetAddr.SetToolTip("Select node address")
		self.Bind(wx.EVT_BUTTON, self.onGetNodeAddr, self.bGetAddr)
		hsizer.Add(self.bGetAddr)
		hsizer.AddSpacer(10)
	
		self.bRefresh = wx.Button(self, wx.ID_ANY, "Refresh")
		self.bRefresh.SetToolTip("Refresh node information by querying the actual node")
		self.Bind(wx.EVT_BUTTON, self.onBRefresh, self.bRefresh)
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
		hsizer.Add(wx.StaticText(boxCfg, wx.ID_ANY, "Outputs:", size=(CFGLABELW, -1)))
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
		
		sz.AddSpacer(20)
		
		mainsz = wx.BoxSizer(wx.HORIZONTAL)
		mainsz.AddSpacer(20)
		mainsz.Add(sz)
		mainsz.AddSpacer(20)
		
		wsz = wx.BoxSizer(wx.VERTICAL)
		wsz.Add(mainsz)
		
		self.SetSizer(wsz)
		
		self.Layout()
		self.Fit()
		self.Show()
		
		self.enableMenuItems(False)
		
		self.server.setServerAddress(self.teIpAddr.GetValue(), self.teHPort.GetValue())
		self.serverValueChanged = False
		self.hPortValueChanged = False
		
		self.timer.Start(1000)
		self.Bind(wx.EVT_TIMER, self.onTimer)
		self.Bind(EVT_DELIVERY, self.onDeliveryEvent)
		self.Bind(EVT_DISCONNECT, self.onDisconnectEvent)
		
	def onMenuInputs(self, _):
		if self.currentNodeAddr is None:
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
			
		self.dlgInputs =  InputsDlg(self, self.inputsMap, self.inputs, self.currentNodeAddr)
		if pos is not None:
			self.dlgInputs.SetPosition(pos)
		self.dlgInputs.Show()
		
	def dlgInputsExit(self):
		self.dlgInputs = None
		
	def onMenuOutputs(self, _):
		if self.currentNodeAddr is None:
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
			
		self.dlgOutputs =  OutputsDlg(self, self.outputsMap, self.outputs, self.currentNodeAddr)
		if pos is not None:
			self.dlgOutputs.SetPosition(pos)
		self.dlgOutputs.Show()
		
	def dlgOutputsExit(self):
		self.dlgOutputs = None
		
	def onMenuServos(self, _):
		if self.currentNodeAddr is None:
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
			
		self.dlgServos =  ServosDlg(self, self.servosMap, self.servos, self.currentNodeAddr)
		if pos is not None:
			self.dlgServos.SetPosition(pos)
		self.dlgServos.Show()
		
	def dlgServosExit(self):
		self.dlgServos = None
		
	def onTeIpAddrSetFocus(self, evt):
		self.serverValueChanged = False
		evt.Skip()
		
	def onTeIpAddrChange(self, _):
		self.serverValueChanged = True
		
	def onTeIpAddrLoseFocus(self, evt):
		if self.serverValueChanged:
			self.serverValueChanged = False
			self.server.setServerAddress(self.teIpAddr.GetValue(), self.teHPort.GetValue())

		evt.Skip()
		
	def onTeHPortSetFocus(self, evt):
		self.hPortValueChanged = False
		evt.Skip()
		
	def onTeHPortChange(self, _):
		self.hPortValueChanged = True
		
	def onTeHPortLoseFocus(self, evt):
		if self.hPortValueChanged:
			self.hPortValueChanged = False
			self.server.setServerAddress(self.teIpAddr.GetValue(), self.teHPort.GetValue())

		evt.Skip()
		
	def throwTurnout(self, tx, throw):
		ip = self.teIpAddr.GetValue()
		pt = self.teHPort.GetValue()
		addr = self.currentNodeAddr

		if throw == "N":
			try:
				sc, data = self.server.setTurnoutNormal(addr, tx)
			except:
				self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
				return False
		elif throw == "R":
			try:
				sc, data = self.server.setTurnoutReverse(addr, tx)
			except:
				self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
				return False
		else: # throw == "T"
			try:
				sc, data = self.server.setTurnoutToggle(addr, tx)
			except:
				self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
				return False
			
		if sc < 400:
			try:
				if throw == "N":
					self.servosMap[tx][3] = self.servosMap[tx][0]
				elif throw == "R":
					self.servosMap[tx][3] = self.servosMap[tx][1]
				else:
					if self.servosMap[tx][3] == self.servosMap[tx][0]:
						self.servosMap[tx][3] = self.servosMap[tx][1]
					if self.servosMap[tx][3] == self.servosMap[tx][1]:
						self.servosMap[tx][3] = self.servosMap[tx][0]
					else:
						# toggle would have done nothing here
						pass
						
				self.setStatusText("Success")
				return True
			except:
				self.setStatusText("Unable to process return data: '%s'" % data)
				return False
		else:
			self.setStatusText("RC <%d> %s" % (sc, data))
			return False
		
	def setServoAngle(self, sx, ang):
		ip = self.teIpAddr.GetValue()
		pt = self.teHPort.GetValue()
		addr = self.currentNodeAddr
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
			self.setStatusText("RC <%d> %s" % (sc, data))
			return False
		
	def setTurnoutLimits(self, tx, norm, rev, ini):
		ip = self.teIpAddr.GetValue()
		pt = self.teHPort.GetValue()
		addr = self.currentNodeAddr
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
			self.setStatusText("RC <%d> %s" % (sc, data))
			return False
		
	def swapTurnout(self, tx):
		ip = self.teIpAddr.GetValue()
		pt = self.teHPort.GetValue()
		addr = self.currentNodeAddr
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
			self.setStatusText("RC <%d> %s" % (sc, data))
			return False

	def nodeStore(self):
		ip = self.teIpAddr.GetValue()
		pt = self.teHPort.GetValue()
		addr = self.currentNodeAddr
		try:
			sc, data = self.server.nodeStore(addr)
		except:
			self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
			return False
			
		if sc < 400:
			self.setStatusText("Success")
			return True
		else:
			self.setStatusText("RC <%d> %s" % (sc, data))
			return False
		
	def getServosMap(self):
		return self.servosMap
			
	def setOutput(self, bn, newState):
		ip = self.teIpAddr.GetValue()
		pt = self.teHPort.GetValue()
		addr = self.currentNodeAddr
		
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
			self.setStatusText("RC <%d> %s" % (sc, data))
			return False
		
	def setConfigValues(self, i, o, s):
		self.inputs = i		
		self.stInputs.SetLabel("%d" % i)
		self.outputs = o
		self.stOutputs.SetLabel("%d" % o)
		self.servos = s
		self.stServos.SetLabel("%d" % s)
		
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
		try:
			jdata = json.loads(data)
		except json.decoder.JSONDecodeError:
			print("Unable to parse (%s)" % data)
			return
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
		if self.clearTimer == 0:
			self.clearTimer = 10
			self.SetStatusText(text)
		else:
			self.qStatus.put(text)
		
	def onGetNodeAddr(self, _):
		dlg = NodeDlg(self, self.currentNodeAddr, self.getNodeRpt())
		rc = dlg.ShowModal()
		if rc == wx.ID_OK:
			n = dlg.getValues()
			
		dlg.Destroy()
		if rc != wx.ID_OK:
			return 

		if n is None:
			return 
		
		self.currentNodeAddr = n
		self.stAddr.SetLabel("%d" % self.currentNodeAddr)		
		self.loadConfig()
		
	def onBRefresh(self, _):
		ip = self.teIpAddr.GetValue()
		pt = self.teHPort.GetValue()
		addr = self.currentNodeAddr
		
		try:
			sc, data = self.server.nodeRefresh(addr)
				
		except:
			self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
			return
		
		if sc >= 400:
			self.setStatusText("RC <%d> %s" % (sc, data))
			return False
			
		self.setStatusText("Refresh Success")
		self.loadConfig()
		
	def loadConfig(self):
		ip = self.teIpAddr.GetValue()
		pt = self.teHPort.GetValue()
		addr = self.currentNodeAddr
		if addr is None:
			self.setStatusText("Select node address first")
			self.enableMenuItems(False)
		
		self.enableMenuItems(True)
		try:
			sc, data = self.server.getConfig(addr)
		except:
			self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
		
		if sc < 400:
			try:
				d = json.loads(data)
				self.setConfigValues(d['inputs'], d['outputs'], d['servos'])
				self.setStatusText("Retrieve Node Config Success")
			except:
				self.setStatusText("Unable to process return data: '%s'" % data)
		else:
			self.setStatusText("RC <%d> %s" % (sc, data))
			
		try:
			sc, data = self.server.getInputs(addr)
		except:
			self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
			return 
		
		if sc < 400:
			try:
				d = json.loads(data)
				self.inputsMap = d["inputs"]["values"]
				self.openInputsDlg()
				self.setStatusText("Retrieve Inputs Success")
			except:
				self.inputsMap = []
				self.setStatusText("Unable to process return data: '%s'" % data)
		else:
			self.setStatusText("RC <%d> %s" % (sc, data))
			
		try:
			sc, data = self.server.getOutputs(addr)
		except:
			self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
			return 
		
		if sc < 400:
			try:
				d = json.loads(data)
				self.outputsMap = d["outputs"]["values"]
				self.openOutputsDlg()
				self.setStatusText("Retrieve Outputs Success")
			except:
				self.outputsMap = []
				self.setStatusText("Unable to process return data: '%s'" % data)
		else:
			self.setStatusText("RC <%d> %s" % (sc, data))
			
		try:
			sc, data = self.server.getTurnouts(addr)
		except:
			self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
			return 
		
		if sc < 400:
			try:
				d = json.loads(data)
				self.servosMap = d["servos"]["values"]
				self.openServosDlg()
				self.setStatusText("Retrieve Turnouts Success")
			except:
				self.servosMap = []
				self.setStatusText("Unable to process return data: '%s'" % data)
		else:
			self.setStatusText("RC <%d> %s" % (sc, data))
			
	def enableMenuItems(self, flag):
		self.menuNode.Enable(MENU_NODE_CONFIG, flag)
		self.menuWindow.Enable(MENU_WINDOW_INPUTS, flag)	
		self.menuWindow.Enable(MENU_WINDOW_OUTPUTS, flag)	
		self.menuWindow.Enable(MENU_WINDOW_SERVOS, flag)
		self.bRefresh.Enable(flag)	
			
	def onDeliveryEvent(self, evt):
		if "inputs" in evt.data:
			imsg = evt.data["inputs"]
			iaddr = imsg["address"]
			
			if iaddr != self.currentNodeAddr:
				return 
			
			if "delta" in imsg and imsg["delta"]:
				vals = imsg["values"]
				if len(vals) > 0:
					for inp, val in vals:
						self.inputsMap[inp] = val
					if self.dlgInputs is not None:
						self.dlgInputs.update(self.inputsMap)
	
			else:
				vals = imsg["values"]
				if len(vals) == len(self.inputsMap):
					self.inputsMap = [x for x in vals]
					if self.dlgInputs is not None:
						self.dlgInputs.update(self.inputsMap)
				else:
					self.setStatusText("Mismatch number of inputs")
					
		elif "outputs" in evt.data:
			omsg = evt.data["outputs"]
			iaddr = omsg["address"]
			
			if iaddr != self.currentNodeAddr:
				return 
			
			if "delta" in omsg and omsg["delta"]:
				vals = omsg["values"]
				if len(vals) > 0:
					for outp, val in vals:
						self.outputsMap[outp] = val
					if self.dlgOutputs is not None:
						self.dlgOutputs.update(self.outputsMap)
						
			else:
				vals = omsg["values"]
				if len(vals) == len(self.outputsMap):
					self.outputsMap = [x for x in vals]
					if self.dlgOutputs is not None:
						self.dlgOutputs.update(self.outputsMap)
				else:
					self.setStatusText("Mismatch number of outputs")
			
		elif "servos" in evt.data:
			smsg = evt.data["servos"]
			iaddr = smsg["address"]
			
			if iaddr != self.currentNodeAddr:
				return 
			
			if "limits" in smsg and smsg["limits"]:
				vals = smsg["values"]
				if len(vals) > 0:
					for outp, v0, v1, v2 in vals:
						self.servosMap[outp][0] = v0
						self.servosMap[outp][1] = v1
						self.servosMap[outp][2] = v2
					if self.dlgServos is not None:
						self.dlgServos.update(self.servosMap)
				
			elif "delta" in smsg and smsg["delta"]:
				vals = smsg["values"]
				if len(vals) > 0:
					for outp, val in vals:
						self.servosMap[outp][3] = val
					if self.dlgServos is not None:
						self.dlgServos.update(self.servosMap)
			else:
				vals = smsg["values"]
				if len(vals) == len(self.servosMap):
					self.servosMap = [x for x in vals]
					if self.dlgServos is not None:
						self.dlgServos.update(self.servosMap)
				else:
					self.setStatusText("Mismatch number of turnouts/servos")
				
		elif "nodes" in evt.data:
			pass
		
		else:
			print("Unknown report type (%s)" % evt.data.keys()[0])
			
	def onMessageEvent(self, evt):
		self.setStatusText(evt.message)
		
	def getNodeRpt(self):
		ip = self.teIpAddr.GetValue()
		pt = self.teHPort.GetValue()
		try:
			sc, data = self.server.getNodeRpt()
		except:
			self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
			return None

		if sc < 400:
			try:
				self.setStatusText("Success")
				d = json.loads(data)
				return d
			except:
				self.setStatusText("Unable to process return data: '%s'" % data)
				return None
		else:
			self.setStatusText("RC <%d> %s" % (sc, data))
			return None
		
	def onMenuNodes(self, _):
		d = self.getNodeRpt()
		if d is None:
			return False
		rpt = ""
		for nd in sorted(d.keys()):
			active = "Active" if d[nd]["active"] else "Inactive" 
			rpt += "%20.20s: A:%-2d   I:%-2d   O:%-2d   S:%-2d   %s\n" % (
				nd, d[nd]["addr"], d[nd]["input"], d[nd]["output"],
				d[nd]["servo"], active)
			
		dlg = wx.MessageDialog(self, rpt, "Nodes Report", wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
		return True
	
	def onMenuConfig(self, _):
		addr = self.currentNodeAddr
		dlg = wx.MessageDialog(self,
					"Proceeding with this will result in the node restarting\nand will require a reconfiguration and restart of the server process",
					"Reconfiguration of Node %d" % addr, wx.OK | wx.CANCEL | wx.ICON_WARNING)
		rc = dlg.ShowModal()
		dlg.Destroy()
		if rc == wx.ID_OK:
			dlg = NodeConfigDlg(self, addr, self.inputs, self.outputs, self.servos)
			rc = dlg.ShowModal()
			if rc == wx.ID_OK:
				a, i, o, s = dlg.getValues()
				
			dlg.Destroy()
			if rc != wx.ID_OK:
				return 
			
			ip = self.teIpAddr.GetValue()
			pt = self.teHPort.GetValue()
			try:
				sc, data = self.server.setConfig(addr, a, i, o, s)
			except:
				self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
				return False
	
			if sc < 400:
				self.setStatusText("Success")
				return True
			else:
				self.setStatusText("RC <%d> %s" % (sc, data))
				return False
			
	def onMenuInit(self, _):
		addr = self.currentNodeAddr
		
		ip = self.teIpAddr.GetValue()
		pt = self.teHPort.GetValue()
		try:
			sc, data = self.server.nodeInit(addr)
		except:
			self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
			return False

		if sc < 400:
			self.setStatusText("Success")
			return True
		else:
			self.setStatusText("RC <%d> %s" % (sc, data))
			return False
			
	def onMenuShutdown(self, _):
		dlg = wx.MessageDialog(self,
					"This will shutdown the server process.\nAre you sure you want to proceed?",
					"Continue with server shutdown", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING)
		rc = dlg.ShowModal()
		dlg.Destroy()
		if rc == wx.ID_YES:
			ip = self.teIpAddr.GetValue()
			pt = self.teHPort.GetValue()
			try:
				sc, data = self.server.quit()
			except:
				self.setStatusText("Unable to connect to node server at address %s:%s" % (ip, pt))
				return False
	
			if sc < 400:
				self.setStatusText("Success")
				return True
			else:
				self.setStatusText("RC <%d> %s" % (sc, data))
				return False
			
	def onTimer(self, _):
		if self.clearTimer is None:
			return 
		
		if self.clearTimer == 0:
			if self.qStatus.empty():
				self.SetStatusText("")
				self.clearTimer = None
			else:
				t = self.qStatus.get()
				self.SetStatusText(t)
				
		elif self.clearTimer >0:
			self.clearTimer -= 1
		
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
