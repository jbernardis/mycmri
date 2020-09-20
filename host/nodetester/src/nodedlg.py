import wx

class NodeDlg(wx.Dialog):
	def __init__(self, parent, startVal, towers):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "Choose Node")
		self.parent = parent
		self.Bind(wx.EVT_CLOSE, self.onClose)
		
		if towers is None:
			choices = [["%d" % i, i] for i in range(1,20)]
			sval = 0
		else:
			choices = []
			cx = 0
			for t in sorted(towers.keys()):
				c = "%s (%d)" % (t, towers[t]["addr"])
				choices.append([c, towers[t]["addr"]])
				if startVal and startVal == towers[t]["addr"]:
					sval = cx
				cx += 1
			if not startVal:
				sval = 0

		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.AddSpacer(30)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		hsizer.AddSpacer(20)
		hsizer.Add(wx.StaticText(self, wx.ID_ANY, "Choose Node: "))
		hsizer.AddSpacer(10)
		
		self.cbAddr = wx.ComboBox(self, 500, "", choices=[], style=wx.CB_READONLY)
		for c in choices:
			self.cbAddr.Append(c[0], c[1])
		self.cbAddr.SetSelection(sval)
		hsizer.Add(self.cbAddr)
						
		vsizer.Add(hsizer)
		vsizer.AddSpacer(20)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(20)
		
		self.bOK = wx.Button(self, wx.ID_ANY, "OK")
		hsizer.Add(self.bOK)
		self.Bind(wx.EVT_BUTTON, self.onBOK, self.bOK)
		
		hsizer.AddSpacer(20)
		
		self.bCancel = wx.Button(self, wx.ID_ANY, "Cancel")
		hsizer.Add(self.bCancel)
		self.Bind(wx.EVT_BUTTON, self.onBCancel, self.bCancel)
		hsizer.AddSpacer(20)

		vsizer.Add(hsizer)
		vsizer.AddSpacer(30)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(10)
		hsizer.Add(vsizer)
		hsizer.AddSpacer(10)
		
		self.SetSizer(hsizer)
		self.Layout()
		self.Fit()
		
	def getValues(self):
		return self.cbAddr.GetClientData(self.cbAddr.GetSelection())
		
	def onBOK(self, _):
		self.EndModal(wx.ID_OK)
		
	def onBCancel(self, _):
		self.EndModal(wx.ID_CANCEL)
		
	def onClose(self, _):
		self.EndModal(wx.ID_CANCEL)

