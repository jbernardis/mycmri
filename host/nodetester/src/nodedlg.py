import wx

ID_INIT = 8000

class NodeDlg(wx.Dialog):
	def __init__(self, parent, startVal, nodeRpt):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "Choose Node")
		self.parent = parent
		self.Bind(wx.EVT_CLOSE, self.onClose)
		
		nodes = nodeRpt["nodes"]

		if nodes is None:
			self.choices = []
			sval = None
		else:
			self.choices = []
			cx = 0
			for n in nodes:
				nid = "%s (%s)" % (n["name"], n["address"])
				if not n["active"]:
					nid += " *"
				self.choices.append([nid, n["address"], n["active"]])
				if startVal and startVal == n["address"]:
						sval = cx
				cx += 1
					
			if not startVal:
				if len(self.choices) > 0:
					sval = 0
				else:
					sval = None

		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.AddSpacer(30)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		hsizer.AddSpacer(20)
		hsizer.Add(wx.StaticText(self, wx.ID_ANY, "Choose Node: "))
		hsizer.AddSpacer(10)
		
		self.cbAddr = wx.ComboBox(self, 500, "", choices=[], style=wx.CB_READONLY)
		self.Bind(wx.EVT_COMBOBOX, self.onComboBox, self.cbAddr)

		for c in self.choices:
			self.cbAddr.Append(c[0], c[1])
			
		hsizer.Add(self.cbAddr)
						
		vsizer.Add(hsizer)
		vsizer.AddSpacer(20)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(20)
		
		self.bOK = wx.Button(self, wx.ID_ANY, "OK")
		hsizer.Add(self.bOK)
		self.Bind(wx.EVT_BUTTON, self.onBOK, self.bOK)
		self.bOK.Enable(False)
		
		hsizer.AddSpacer(10)
		
		self.bInit = wx.Button(self, wx.ID_ANY, "Init")
		hsizer.Add(self.bInit)
		self.Bind(wx.EVT_BUTTON, self.onBInit, self.bInit)
		self.bInit.Enable(False)
		
		hsizer.AddSpacer(10)
		
		self.bCancel = wx.Button(self, wx.ID_ANY, "Cancel")
		hsizer.Add(self.bCancel)
		self.Bind(wx.EVT_BUTTON, self.onBCancel, self.bCancel)
		hsizer.AddSpacer(20)

		if not sval is None:
			self.cbAddr.SetSelection(sval)
			if self.choices[sval][2]:
				self.bOK.Enable(True)
			else:
				self.bInit.Enable(True)
				
		vsizer.Add(hsizer)
		vsizer.AddSpacer(30)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(10)
		hsizer.Add(vsizer)
		hsizer.AddSpacer(10)
		
		self.SetSizer(hsizer)
		self.Layout()
		self.Fit()
		
	def onComboBox(self, _):
		sv = self.cbAddr.GetSelection()
		if sv == wx.NOT_FOUND:
			self.bOK.Enable(False)
			self.bInit.Enable(False)
		else:
			if self.choices[sv][2]:
				self.bOK.Enable(True)
				self.bInit.Enable(False)
			else:
				self.bOK.Enable(False)
				self.bInit.Enable(True)

		
	def getValues(self):
		sv = self.cbAddr.GetSelection()
		if sv == wx.NOT_FOUND:
			return None
		
		return self.cbAddr.GetClientData(sv)
		
	def onBOK(self, _):
		self.EndModal(wx.ID_OK)
		
	def onBInit(self, _):
		self.EndModal(ID_INIT)
		
	def onBCancel(self, _):
		self.EndModal(wx.ID_CANCEL)
		
	def onClose(self, _):
		self.EndModal(wx.ID_CANCEL)

