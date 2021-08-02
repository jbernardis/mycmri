import wx



class OutputsDlg(wx.Dialog):
	def __init__(self, parent, data, noutputs, addr):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "Outputs for node %d" % addr)
		self.parent = parent
		self.images = parent.images
		self.addr = addr
		self.data = data[:]
		self.noutputs = noutputs
		self.Bind(wx.EVT_CLOSE, self.onClose)
		
		self.nbits = self.noutputs;
		if self.nbits != len(data):
			self.parent.setStatusText("Configuration mismatch")
			maxbit = min(self.nbits, len(data))
		else:
			maxbit = self.nbits
		
		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.AddSpacer(10)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.Add(wx.StaticText(self, wx.ID_ANY, "%2d" % 0, size=(20, -1), style=wx.ALIGN_RIGHT), 0, wx.TOP, 8)
		hsizer.AddSpacer(5)
		
		self.bmpMap = []
		self.pulseLen = []
		
		for i in range(maxbit):
			if i != 0 and i%8 == 0:
				hsizer.AddSpacer(5)
				hsizer.Add(wx.StaticText(self, wx.ID_ANY, "%2d" % (i-1), size=(20, -1), style=wx.ALIGN_LEFT), 0, wx.TOP, 8)
				vsizer.Add(hsizer)
				vsizer.AddSpacer(2)
				hsizer = wx.BoxSizer(wx.HORIZONTAL)
				hsizer.Add(wx.StaticText(self, wx.ID_ANY, "%2d" % i, size=(20, -1), style=wx.ALIGN_RIGHT), 0, wx.TOP, 8)
				hsizer.AddSpacer(5)
			elif i != 0 and i%4 == 0:
				hsizer.AddSpacer(10)
			
			if data[i]:
				png = self.images.pngOutputon
			else:
				png = self.images.pngOutputoff
					
			bmp = wx.BitmapButton(self, wx.ID_ANY, png)
			bmp.SetToolTip("Output %d" % i)
			bmp.myIndex = i
			bmp.Bind(wx.EVT_BUTTON,  self.onBOutput)
			bmp.Bind(wx.EVT_RIGHT_DOWN, self.onBPulse)

			hsizer.Add(bmp)
			hsizer.AddSpacer(2)
			self.bmpMap.append(bmp)
			self.pulseLen.append(0)
						
		hsizer.AddSpacer(5)
		hsizer.Add(wx.StaticText(self, wx.ID_ANY, "%2d" % (maxbit-1), size=(20, -1), style=wx.ALIGN_LEFT), 0, wx.TOP, 8)
		vsizer.Add(hsizer)
		
		vsizer.AddSpacer(10)
		
		self.scPl = wx.SpinCtrl(self, wx.ID_ANY, "1")
		self.scPl.SetRange(1,255)
		self.scPl.SetValue(1)
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(10)
		hsizer.Add(wx.StaticText(self, wx.ID_ANY, "Pulse Length: "), 0, wx.TOP, 8)
		hsizer.Add(self.scPl)
		hsizer.Add(wx.StaticText(self, wx.ID_ANY, " (right-click)"), 0, wx.TOP, 8)
		vsizer.Add(hsizer)
		vsizer.AddSpacer(10)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(10)
		hsizer.Add(vsizer)
		hsizer.AddSpacer(10)
		
		
		self.SetSizer(hsizer)
		self.Layout()
		self.Fit()
		
	def onBPulse(self, event):
		pl = self.scPl.GetValue()
		bn = event.GetEventObject().myIndex
		self.parent.pulseOutput(bn, pl)
		self.pulseOutput(bn, pl)
		
	def onBOutput(self, event):
		bn = event.GetEventObject().myIndex
		on = self.data[bn]
		
		newState = not on
		if self.parent.setOutput(bn, newState):
			self.data[bn] = newState
			if newState:
				png = self.images.pngOutputon
			else:
				png = self.images.pngOutputoff
				
			self.bmpMap[bn].SetBitmap(png)
		
		
	def update(self, data):
		if len(data) != len(self.data):
			self.parent.setStatusText("Configuration changed")
			maxbit = min(self.nbits, len(data))
		else:
			maxbit = self.nbits
			
		for i in range(maxbit):
			if data[i] != self.data[i]:
				self.data[i] = data[i]
				if data[i]:
					png = self.images.pngOutputon
				else:
					png = self.images.pngOutputoff
					
				self.bmpMap[i].SetBitmap(png)
				
	def pulseOutput(self, ox, pl):
		self.bmpMap[ox].SetBitmap(self.images.pngOutputon)
		self.pulseLen[ox] = pl + 1
		self.data[ox] = True
		
	def clearPulses(self):
		for i in range(len(self.pulseLen)):
			if self.pulseLen[i] > 0:
				self.pulseLen[i] -= 1
				if self.pulseLen[i] == 0:
					self.bmpMap[i].SetBitmap(self.images.pngOutputoff)
					self.data[i] = False
		
	def onClose(self, _):
		self.parent.dlgOutputsExit()
		self.Destroy()

