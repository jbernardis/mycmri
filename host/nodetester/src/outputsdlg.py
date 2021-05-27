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
		
		self.bmpMap = []
		
		for i in range(maxbit):
			if i != 0 and i%8 == 0:
				vsizer.Add(hsizer)
				vsizer.AddSpacer(2)
				hsizer = wx.BoxSizer(wx.HORIZONTAL)
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
			hsizer.Add(bmp)
			hsizer.AddSpacer(2)
			self.bmpMap.append(bmp)
						
		vsizer.Add(hsizer)
		
		vsizer.AddSpacer(10)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(10)
		hsizer.Add(vsizer)
		hsizer.AddSpacer(10)
		
		
		self.SetSizer(hsizer)
		self.Layout()
		self.Fit()
		
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
		
		
	def onClose(self, _):
		self.parent.dlgOutputsExit()
		self.Destroy()

