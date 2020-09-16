import wx



class ToConfigDlg(wx.Dialog):
	def __init__(self, parent, sn, sr, si):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "Enter Angles for Turnout(s)")
		self.parent = parent
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.useNormForIni = sn == si
		
		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.AddSpacer(30)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		hsizer.AddSpacer(20)
		st = wx.StaticText(self, wx.ID_ANY, "Enter normal Angle: ", size=(116, -1))
		hsizer.Add(st)
		hsizer.AddSpacer(10)
		
		self.scNormal = wx.SpinCtrl(self, wx.ID_ANY, "")
		self.scNormal.SetRange(0,180)
		self.scNormal.SetValue(sn)
		hsizer.Add(self.scNormal)
						
		vsizer.Add(hsizer)
		vsizer.AddSpacer(10)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		hsizer.AddSpacer(20)
		st = wx.StaticText(self, wx.ID_ANY, "Enter reverse Angle: ", size=(116, -1))
		hsizer.Add(st)
		hsizer.AddSpacer(10)
		
		self.scReverse = wx.SpinCtrl(self, wx.ID_ANY, "")
		self.scReverse.SetRange(0,180)
		self.scReverse.SetValue(sr)
		hsizer.Add(self.scReverse)
						
		vsizer.Add(hsizer)
		vsizer.AddSpacer(10)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		hsizer.AddSpacer(20)
		st = wx.StaticText(self, wx.ID_ANY, "Enter initial Angle: ", size=(116, -1))
		hsizer.Add(st)
		hsizer.AddSpacer(10)
		
		self.scInitial = wx.SpinCtrl(self, wx.ID_ANY, "")
		self.scInitial.SetRange(0,180)
		self.scInitial.SetValue(si)
		hsizer.Add(self.scInitial)
		self.scInitial.Enable(not self.useNormForIni)
						
		vsizer.Add(hsizer)
		vsizer.AddSpacer(5)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(20)
		self.cbUseNorm = wx.CheckBox(self, wx.ID_ANY, "Use Normal value for Initial")
		self.cbUseNorm.SetValue(self.useNormForIni)
		hsizer.Add(self.cbUseNorm)
		self.Bind(wx.EVT_CHECKBOX, self.onCbUseNorm, self.cbUseNorm)
		
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
		
	def onCbUseNorm(self, _):
		self.useNormForIni = self.cbUseNorm.GetValue()
		self.scInitial.Enable(not self.useNormForIni)
		
	def getValues(self):
		n = self.scNormal.GetValue()
		r = self.scReverse.GetValue()
		if self.cbUseNorm.GetValue():
			i = n
		else:
			i = self.scInitial.GetValue()
			
		return n, r, i
		
	def onBOK(self, _):
		self.EndModal(wx.ID_OK)
		
	def onBCancel(self, _):
		self.EndModal(wx.ID_CANCEL)
		
	def onClose(self, _):
		self.EndModal(wx.ID_CANCEL)

