import wx



class InputsDlg(wx.Dialog):
	def __init__(self, parent, data, ninputs, addr):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "Inputs for node %d" % addr)
		self.parent = parent
		self.images = parent.images
		self.data = data[:]
		self.ninputs = ninputs
		self.Bind(wx.EVT_CLOSE, self.onClose)
		
		self.nbits = self.ninputs*8;
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
				png = self.images.pngInputoff
			else:
				png = self.images.pngInputon
					
			bmp = wx.StaticBitmap(self, wx.ID_ANY, png)
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
					png = self.images.pngInputoff
				else:
					png = self.images.pngInputon
					
				self.bmpMap[i].SetBitmap(png)
		
		
	def onClose(self, _):
		self.parent.dlgInputsExit()
		self.Destroy()

