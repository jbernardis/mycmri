import wx
import os



class NodeConfigDlg(wx.Dialog):
	def __init__(self, parent, addr, si, so, ss):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "Node %d Re-Configuration" % addr)
		self.parent = parent
		self.currentAddr = addr
		self.Bind(wx.EVT_CLOSE, self.onClose)
		
		if os.name == 'nt':
			stSize = (140, -1)
		else:
			stSize = (140, -1)

		
		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.AddSpacer(20)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)		
		hsizer.AddSpacer(10)
		hsizer.Add(wx.StaticText(self, wx.ID_ANY, "New Node Address:", size=stSize))
		hsizer.AddSpacer(10)
		self.scAddress = wx.SpinCtrl(self, wx.ID_ANY, "", (30, 50))
		self.scAddress.SetRange(1,100)
		self.scAddress.SetValue(addr)
		hsizer.Add(self.scAddress)
		
		vsizer.Add(hsizer)
		vsizer.AddSpacer(10)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)		
		hsizer.AddSpacer(10)
		hsizer.Add(wx.StaticText(self, wx.ID_ANY, "Number of Input Bytes:", size=stSize))
		hsizer.AddSpacer(10)
		self.scInputs = wx.SpinCtrl(self, wx.ID_ANY, "", (30, 50))
		self.scInputs.SetRange(0,16)
		self.scInputs.SetValue(si)
		hsizer.Add(self.scInputs)
		
		vsizer.Add(hsizer)
		vsizer.AddSpacer(10)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)		
		hsizer.AddSpacer(10)
		hsizer.Add(wx.StaticText(self, wx.ID_ANY, "Number of Output Bytes:", size=stSize))
		hsizer.AddSpacer(10)
		self.scOutputs = wx.SpinCtrl(self, wx.ID_ANY, "", (30, 50))
		self.scOutputs.SetRange(0,16)
		self.scOutputs.SetValue(so)
		hsizer.Add(self.scOutputs)
		
		vsizer.Add(hsizer)
		vsizer.AddSpacer(10)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)		
		hsizer.AddSpacer(10)
		hsizer.Add(wx.StaticText(self, wx.ID_ANY, "Number of Servo Boards:", size=stSize))
		hsizer.AddSpacer(10)
		self.scServos = wx.SpinCtrl(self, wx.ID_ANY, "", (30, 50))
		self.scServos.SetRange(0,16)
		self.scServos.SetValue(ss)
		hsizer.Add(self.scServos)
		
		vsizer.Add(hsizer)
		vsizer.AddSpacer(30)
		
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
		vsizer.AddSpacer(20)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(10)
		hsizer.Add(vsizer)
		hsizer.AddSpacer(10)
		
		self.SetSizer(hsizer)
		self.Layout()
		self.Fit()
		
	def getValues(self):
		a = self.scAddress.GetValue()
		i = self.scInputs.GetValue()
		o = self.scOutputs.GetValue()
		s = self.scServos.GetValue()
			
		return a, i, o, s
		
	def onBOK(self, _):
		self.EndModal(wx.ID_OK)
		
	def onBCancel(self, _):
		self.EndModal(wx.ID_CANCEL)
		
	def onClose(self, _):
		self.EndModal(wx.ID_CANCEL)

