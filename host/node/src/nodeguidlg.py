import wx
from turnoutdlg import TurnoutDlg
from servoangledlg import ServoAngleDlg

class NodeGuiDlg(wx.Frame):
	def __init__(self, parent,  node):
		title = "Node %d (%s) %d inputs/%d outputs/%d servos" % (node.addr, node.tty, node.inputs, node.outputs, node.servos)
		wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(500, 500))
		self.SetBackgroundColour(wx.Colour(255, 255, 255))
		self.parent = parent
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.node = node
		self.node.registerCallback(self.inputRcvd, self.identityRcvd, self.getTurnoutRcvd, self.storeRcvd, self.msgRcvd)
		
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.onTimer, self.timer)
		
		self.connected = False
		self.polling = False
		self.turnoutDlg = None
		self.callbackInput = None
		
		sz = wx.BoxSizer(wx.VERTICAL)
		sz.AddSpacer(20)
		
		self.bConnect = wx.Button(self, wx.ID_ANY, "Disconnect")
		self.Bind(wx.EVT_BUTTON, self.onConnect, self.bConnect)
		self.bPoll = wx.Button(self, wx.ID_ANY, "Pause Poll")
		self.Bind(wx.EVT_BUTTON, self.onPoll, self.bPoll)
		self.bPoll.Enable(False)
		self.bTurnout = wx.Button(self, wx.ID_ANY, "Turnouts")
		self.Bind(wx.EVT_BUTTON, self.onTurnout, self.bTurnout)
		self.bTurnout.Enable(False)
		
		lhsz = wx.BoxSizer(wx.HORIZONTAL)
		lhsz.AddSpacer(5)
		lhsz.Add(self.bConnect)
		lhsz.AddSpacer(10)
		lhsz.Add(self.bPoll)
		lhsz.AddSpacer(10)
		lhsz.Add(self.bTurnout)
		sz.Add(lhsz)
		sz.AddSpacer(20)
		
		oBox = wx.StaticBox(self, wx.ID_ANY, " Inputs ")
		bsizer = wx.BoxSizer(wx.VERTICAL)
		topBorder = oBox.GetBordersForSizer()[0]
		bsizer.AddSpacer(topBorder)
		
		hsizer = None
		self.cbInput = []
		for i in range(self.node.inputs*8):
			if i % 8 == 0:
				if hsizer is not None:
					hsizer.AddSpacer(20)
					bsizer.Add(hsizer)
					bsizer.AddSpacer(10)
				hsizer = wx.BoxSizer(wx.HORIZONTAL)
				hsizer.AddSpacer(10)
				
			cb = wx.CheckBox(oBox, wx.ID_ANY, " %d:" % i, size=(50, -1), style=wx.ALIGN_RIGHT)
			hsizer.Add(cb)
			self.Bind(wx.EVT_CHECKBOX, self.onCbInput, cb)
			self.cbInput.append(cb)
			
		bsizer.Add(hsizer)
		bsizer.AddSpacer(30)
		oBox.SetSizer(bsizer)
		oBox.Layout()
		oBox.Fit()
		
		sz.Add(oBox)
		sz.AddSpacer(20)
		
		oBox = wx.StaticBox(self, wx.ID_ANY, " Outputs ")
		bsizer = wx.BoxSizer(wx.VERTICAL)
		topBorder = oBox.GetBordersForSizer()[0]
		bsizer.AddSpacer(topBorder)
		
		hsizer = None
		self.cbOutput = []
		for i in range(self.node.outputs*8):
			if i % 8 == 0:
				if hsizer is not None:
					hsizer.AddSpacer(20)
					bsizer.Add(hsizer)
					bsizer.AddSpacer(10)
				hsizer = wx.BoxSizer(wx.HORIZONTAL)
				hsizer.AddSpacer(20)
				
			cb = wx.CheckBox(oBox, wx.ID_ANY, "%d:" % i, size=(50, -1), style=wx.ALIGN_RIGHT)
			hsizer.Add(cb)
			self.Bind(wx.EVT_CHECKBOX, self.onCbOutput, cb)
			self.cbOutput.append(cb)
			
		bsizer.Add(hsizer)
		bsizer.AddSpacer(30)
		oBox.SetSizer(bsizer)
		oBox.Layout()
		oBox.Fit()
		
		sz.Add(oBox)
		sz.AddSpacer(20)

		
		oBox = wx.StaticBox(self, wx.ID_ANY, " Turnouts ")
		bsizer = wx.BoxSizer(wx.VERTICAL)
		topBorder = oBox.GetBordersForSizer()[0]
		bsizer.AddSpacer(topBorder)
		
		hsizer = None
		self.cbTurnout = []
		for i in range(self.node.servos*16):
			if i % 8 == 0:
				if hsizer is not None:
					hsizer.AddSpacer(20)
					bsizer.Add(hsizer)
					bsizer.AddSpacer(10)
				hsizer = wx.BoxSizer(wx.HORIZONTAL)
				hsizer.AddSpacer(20)
				
			cb = wx.CheckBox(oBox, wx.ID_ANY, "%d:" % i, size=(50, -1), style=wx.ALIGN_RIGHT)
			hsizer.Add(cb)
			self.Bind(wx.EVT_CHECKBOX, self.onCbTurnout, cb)
			self.cbTurnout.append(cb)
			
		bsizer.Add(hsizer)
		bsizer.AddSpacer(30)
		oBox.SetSizer(bsizer)
		oBox.Layout()
		oBox.Fit()
		
		sz.Add(oBox)
		sz.AddSpacer(20)
		
		self.bAngle = wx.Button(self, wx.ID_ANY, "Servo Angle")
		self.Bind(wx.EVT_BUTTON, self.onAngle, self.bAngle)
		self.bAngle.Enable(False)
		sz.Add(self.bAngle)
		sz.AddSpacer(20)
		
		hsz = wx.BoxSizer(wx.HORIZONTAL)
		hsz.AddSpacer(20)
		hsz.Add(sz)
		hsz.AddSpacer(20)
		
		self.enableButtons(False)
		self.SetSizer(hsz)
		
		self.Layout()
		self.Fit()
		s = self.GetSize()
		s[1] += 50
		self.SetSize(s)
		
		self.initNode()

		self.Show()

	def initNode(self):
		self.node.setPoll(True)
		self.node.getCurrentInput()
		self.polling = True
		self.timer.Start(250)
		self.bPoll.Enable(True)
		self.bPoll.SetLabel("Pause Poll")					
		self.bTurnout.Enable(True)
		self.enableButtons()			

	
	def enableButtons(self, flag=True):
		self.bAngle.Enable(flag)
		for w in self.cbInput:
			w.Enable(flag)
			
		for w in self.cbOutput:
			w.Enable(flag)
			
		for w in self.cbTurnout:
			w.Enable(flag)
			
	def onTimer(self, _):
		self.node.process()

	def inputRcvd(self, addr, inp, val, delta):
		self.cbInput[inp].SetValue(val==1)
		
		if not self.callbackInput is None:
			self.callbackInput(addr, inp, val, delta)
			
	def setTurnout(self, tx, val):
		self.cbTurnout[tx].SetValue(val);
		if val:
			self.node.setTurnoutReverse(tx)
		else:
			self.node.setTurnoutNormal(tx)
			
	def setOutput(self, ox, val):
		self.cbOutput[ox].SetValue(val);
		if val:
			self.node.setOutputOn(ox)
		else:
			self.node.setOutputOff(ox)

	def setAngle(self, sx, a):
		self.node.setAngle(sx, a)
			
	def registerInputs(self, cb):
		self.callbackInput = cb
			
	def identityRcvd(self, addr, inp, outp, servo):
		msg = "Configuration received:\n  Addr: %d" % addr
		if addr != self.node.addr:
			msg += " (does not equal current value of %d)" % self.node.addr
		msg += "\n"
			
		msg += "  Inputs: %d - %d channels" % (inp, inp*8)
		if inp != self.node.inputs:
			msg += " (does not match current value of %d)" % self.node.inputs
		msg += "\n"
			
		msg += "  Outputs: %d - %d channels" % (outp, outp*8)
		if outp != self.node.outputs:
			msg += " (does not match current value of %d)" % self.node.outputs
		msg += "\n"
		
		msg += "  Servos: %d - %d channels" % (servo, servo*16)	
		if servo != self.node.servos:
			msg += " (does not match current value of %d)" % servo, self.node.servos
			
		dlg = wx.MessageDialog(self, msg, "Node Configuration Report",
							   wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()
			
	def getTurnoutRcvd(self, addr, tx, norm, rev, ini):
		if self.turnoutDlg is None:
			msg = "Turnout %d:\n Normal: %d\n Reverse: %d\n Initial: %d" % (tx, norm, rev, ini)
			dlg = wx.MessageDialog(self, msg, "Turnout Configuration Report",
								   wx.OK | wx.ICON_INFORMATION)
			dlg.ShowModal()
			dlg.Destroy()
		else:
			self.turnoutDlg.insertRetrievedValues(norm, rev, ini)
			
	def storeRcvd(self, addr, res):
		for i in range(0, len(res), 3):
			print("Turnout %d: %d/%d/%d" % (int(i/3), res[i], res[i+1], res[i+2]))

	def msgRcvd(self, addr, cmd, msg):
		s = "RCV  %02x: " % ord(cmd)	
		for c in msg:
			s += "%02x " % c
		print(s)

	def onConnect(self, _):
		self.closeDlg()

	def onPoll(self, _):
		self.polling = not self.polling
		if self.polling:
			self.bPoll.SetLabel("Pause Poll")
		else:
			self.bPoll.SetLabel("Resume Poll")
		self.node.setPoll(self.polling)
		
	def onTurnout(self, _):
		self.turnoutDlg = TurnoutDlg(self, self.node, self.node.servos*16)
		self.turnoutDlg.ShowModal()
		self.turnoutDlg.Destroy()
		self.turnoutDlg = None

	def onAngle(self, _):
		dlg = ServoAngleDlg(self, self.node, self.node.servos*16)
		dlg.ShowModal()
		dlg.Destroy()
		
	def onCbInput(self, evt):
		cb = evt.GetEventObject()
		cb.SetValue(not cb.GetValue())
		
	def onCbOutput(self, evt):
		cb = evt.GetEventObject()
		flag = cb.IsChecked()
		ox = int(cb.GetLabel().split(":")[0])
		if flag:
			self.node.setOutputOn(ox)
		else:
			self.node.setOutputOff(ox)
					
	def onCbTurnout(self, evt):
		cb = evt.GetEventObject()
		flag = cb.IsChecked()
		tx = int(cb.GetLabel().split(":")[0])
		if flag:
			self.node.setTurnoutReverse(tx)
		else:
			self.node.setTurnoutNormal(tx)
			
	def onClose(self, _):
		self.closeDlg()
		
	def closeDlg(self):
		self.parent.nodeDlgClose(self.node.tty)
		try:
			self.timer.Stop()
		except:
			pass

		try:
			self.timer.Destroy()
		except:
			pass

		try:
			self.node.stop()
		except:
			pass

		try:
			self.node.disconnect()
		except:
			pass

		self.Destroy()
