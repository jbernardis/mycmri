import wx



class AngleDlg(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "Enter Angle for servo(s)")
		self.parent = parent
		self.Bind(wx.EVT_CLOSE, self.onClose)
		
		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.AddSpacer(30)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		hsizer.AddSpacer(20)
		hsizer.Add(wx.StaticText(self, wx.ID_ANY, "Enter target Angle: "))
		hsizer.AddSpacer(10)
		
		self.scAngle = wx.SpinCtrl(self, wx.ID_ANY, "")
		self.scAngle.SetRange(0,180)
		self.scAngle.SetValue(90)
		hsizer.Add(self.scAngle)
						
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
		return self.scAngle.GetValue()
		
	def onBOK(self, _):
		self.EndModal(wx.ID_OK)
		
	def onBCancel(self, _):
		self.EndModal(wx.ID_CANCEL)
		
	def onClose(self, _):
		self.EndModal(wx.ID_CANCEL)

