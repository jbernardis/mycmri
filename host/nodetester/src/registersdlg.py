import wx



class RegistersDlg(wx.Dialog):
	def __init__(self, parent, registers, nregisters, addr):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "Registers for node %d" % addr)
		self.parent = parent
		self.images = parent.images
		self.addr = addr
		self.registers = registers[:]
		self.nregisters = nregisters
		self.Bind(wx.EVT_CLOSE, self.onClose)
		
		if self.nregisters != len(self.registers):
			self.parent.setStatusText("Configuration mismatch")
			maxreg = min(self.nregisters, len(registers))
		else:
			maxreg = self.nregisters
		
		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.AddSpacer(10)
		
		self.te = []
		
		for i in range(maxreg):
			hsizer = wx.BoxSizer(wx.HORIZONTAL)
			hsizer.Add(wx.StaticText(self, wx.ID_ANY, "%-2d:" % i))
			hsizer.AddSpacer(10)
			te = wx.TextCtrl(self, wx.ID_ANY, self.registers[i])
			self.te.append(te)
			hsizer.Add(te)
			hsizer.AddSpacer(10)
			
			b = wx.Button(self, wx.ID_ANY, "Set", size=(50, -1))
			b.registerIndex = i
			self.Bind(wx.EVT_BUTTON, self.OnBSet, b)
			hsizer.Add(b)
			
			vsizer.Add(hsizer)
		
		vsizer.AddSpacer(10)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(10)
		hsizer.Add(vsizer)
		hsizer.AddSpacer(10)
		
		
		self.SetSizer(hsizer)
		self.Layout()
		self.Fit()
		
	def OnBSet(self, evt):
		rx = evt.GetEventObject().registerIndex
		val = self.te[rx].GetValue()
		self.parent.setRegister(rx, val)

	def update(self, registers):
		if len(registers) != len(self.registers):
			self.parent.setStatusText("Configuration changed")
			maxreg = min(self.nregisters, len(registers))
		else:
			maxreg = self.nregisters
			
		for i in range(maxreg):
			if registers[i] != self.registers[i]:
				self.registers[i] = registers[i]
				self.te[i].SetValue(self.registers[i])
		
		
	def onClose(self, _):
		self.parent.dlgRegistersExit()
		self.Destroy()

