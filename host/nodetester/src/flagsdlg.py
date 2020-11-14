import wx

class FlagsDlg(wx.Dialog):
	def __init__(self, parent, data, nflags, addr):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "Flags for node %d" % addr)
		self.parent = parent
		self.images = parent.images
		self.addr = addr
		self.data = data[:]
		self.nflags = nflags
		self.Bind(wx.EVT_CLOSE, self.onClose)
		
		if self.nflags != len(data):
			self.parent.setStatusText("Configuration mismatch")
			maxflag = min(self.nflagss, len(data))
		else:
			maxflag = self.nflags
		
		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.AddSpacer(10)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		self.bmpMap = []
		
		for i in range(maxflag):
			if i != 0 and i%8 == 0:
				vsizer.Add(hsizer)
				vsizer.AddSpacer(2)
				hsizer = wx.BoxSizer(wx.HORIZONTAL)
			elif i != 0 and i%4 == 0:
				hsizer.AddSpacer(10)
			
			if data[i]:
				png = self.images.pngFlagon
			else:
				png = self.images.pngFlagoff
				
					
			bmp = wx.BitmapButton(self, wx.ID_ANY, png)
			bmp.SetToolTip("Flag %d" % i)
			bmp.myIndex = i
			bmp.Bind(wx.EVT_BUTTON,  self.onBFlag)
			hsizer.Add(bmp)
			hsizer.AddSpacer(2)
			self.bmpMap.append(bmp)
			
		if maxflag < 8:
			nspaces = 8 - maxflag
			spacerw = 24 * nspaces
			if nspaces > 4:
				spacerw += 10
			hsizer.AddSpacer(spacerw)
						
		vsizer.Add(hsizer)
		
		vsizer.AddSpacer(10)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(10)
		hsizer.Add(vsizer)
		hsizer.AddSpacer(10)
		
		
		self.SetSizer(hsizer)
		self.Layout()
		self.Fit()
		
	def onBFlag(self, event):
		bn = event.GetEventObject().myIndex
		on = self.data[bn]
		
		newState = not on
		if self.parent.setFlag(bn, newState):
			self.data[bn] = newState
			if newState:
				png = self.images.pngFlagon
			else:
				png = self.images.pngFlagoff
				
			self.bmpMap[bn].SetBitmap(png)
		
		
	def update(self, data):
		if len(data) != len(self.data):
			self.parent.setStatusText("Configuration changed")
			maxflag = min(self.nflags, len(data))
		else:
			maxflag = self.nflags
			
		for i in range(maxflag):
			if data[i] != self.data[i]:
				self.data[i] = data[i]
				if data[i]:
					png = self.images.pngFlagon
				else:
					png = self.images.pngFlagoff
					
				self.bmpMap[i].SetBitmap(png)
		
		
	def onClose(self, _):
		self.parent.dlgFlagsExit()
		self.Destroy()

