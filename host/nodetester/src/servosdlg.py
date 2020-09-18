import wx
import os

from angledlg import AngleDlg
from toconfigdlg import ToConfigDlg

colInfo = [
	("", wx.LIST_FORMAT_RIGHT, 20 if os.name == 'nt' else 30),
	("Index", wx.LIST_FORMAT_RIGHT, 40),
	("Normal", wx.LIST_FORMAT_RIGHT, 60),
	("Reverse", wx.LIST_FORMAT_RIGHT, 60),
	("Initial", wx.LIST_FORMAT_RIGHT, 60),
	("Current", wx.LIST_FORMAT_RIGHT, 60)
]


class ServoListCtrl(wx.ListCtrl):
	def __init__(self, parent, data, maxsv):
		colWidth = 0
		nLines = 16
		for c in colInfo:
			colWidth += c[2]
			
		if os.name == 'nt':
			lcSize = (colWidth+18, nLines*19+30)
		else:
			lcSize = (colWidth+18, nLines*19+30)
			
		wx.ListCtrl.__init__(self, parent, wx.ID_ANY, style=wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_VRULES|wx.LC_HRULES, size=lcSize)
		self.parent = parent
		self.maxsv = maxsv
		self.data = data[:]
		self.ctSel = 0
		
		self.EnableCheckBoxes(enable=True)
		for c in colInfo:
			self.AppendColumn(c[0], c[1], c[2])

		self.SetItemCount(maxsv)
		self.isChecked = [False] * maxsv
		
		self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.onColumnResize)
		
		self.attrNorm = wx.ItemAttr()
		self.attrNorm.SetBackgroundColour(wx.Colour(113,244,89))

		self.attrRev = wx.ItemAttr()
		self.attrRev.SetBackgroundColour(wx.Colour(241,54,73))

		self.attrOth = wx.ItemAttr()
		self.attrOth.SetBackgroundColour(wx.Colour(243,240,118))

		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
		
	def onColumnResize(self, evt):
		evt.Veto()
		
	def update(self, data, preserve):
		self.data = data[:]
		if not preserve:
			self.isChecked = [False] * self.maxsv
			
		self.RefreshItems(0, self.maxsv-1)
		self.enableButtons()
		
	def getDataForTurnout(self, tx):
		return self.data[tx]
		
	def getSelectionCount(self):
		return self.ctSel
	
	def getSelection(self):
		return [i for i in range(len(self.isChecked)) if self.isChecked[i]]
	
	def selectAll(self):
		self.isChecked = [True] * self.maxsv
		self.RefreshItems(0, self.maxsv-1)
		self.parent.enableButtons(self.maxsv)
		
	def selectNone(self):
		self.isChecked = [False] * self.maxsv
		self.RefreshItems(0, self.maxsv-1)
		self.parent.enableButtons(0)
		
	def OnItemActivated(self, event):
		item = event.Index
		self.isChecked[item] = not self.isChecked[item]
		self.enableButtons()
		self.Select(item, 0)
		self.RefreshItem(item)
		
	def enableButtons(self):
		self.ctSel = 0
		for sel in self.isChecked:
			if sel:
				self.ctSel += 1
		self.parent.enableButtons(self.ctSel)

	def OnGetItemIsChecked(self, item):
		return self.isChecked[item]
		
	def OnGetItemText(self, item, col):
		if col == 0:
			return ""
		elif col == 1:
			return "%2d" % item
		else:
			return "%3d" % self.data[item][col-2]

	def OnGetItemAttr(self, item):
		sv = self.data[item]
		
		if sv[3] == sv[0]:
			return self.attrNorm
		elif sv[3] == sv[1]:
			return self.attrRev
		else:
			return self.attrOth



class ServosDlg(wx.Dialog):
	def __init__(self, parent, data, nservos, addr):
		wx.Dialog.__init__(self, parent, wx.ID_ANY, "Turnouts/Servos for node %d" % addr)
		self.parent = parent
		self.images = parent.images
		self.addr = addr
		self.nservos = nservos
		self.Bind(wx.EVT_CLOSE, self.onClose)
		
		self.nbits = self.nservos*16
		if self.nbits != len(data):
			self.parent.setStatusText("Configuration mismatch")
			maxbit = min(self.nbits, len(data))
		else:
			maxbit = self.nbits
		
		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.AddSpacer(10)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		self.lcServos = ServoListCtrl(self, data, maxbit)

		hsizer.Add(self.lcServos, 1, wx.EXPAND)
		
		vsizer.Add(hsizer)
		
		vsizer.AddSpacer(10)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(10)
		self.bSelectAll = wx.Button(self, wx.ID_ANY, "Select All")
		hsizer.Add(self.bSelectAll)
		self.Bind(wx.EVT_BUTTON, self.onBSelectAll, self.bSelectAll)
		
		hsizer.AddSpacer(10)
		self.bSelectNone = wx.Button(self, wx.ID_ANY, "Select None")
		hsizer.Add(self.bSelectNone)
		self.Bind(wx.EVT_BUTTON, self.onBSelectNone, self.bSelectNone)
		
		hsizer.AddSpacer(20)
		self.cbPreserve = wx.CheckBox(self, wx.ID_ANY, "Preserve Selections")
		self.cbPreserve.SetToolTip("If set, selections in the above list will NOT be cleared between operations")
		self.cbPreserve.SetValue(False)
		hsizer.Add(self.cbPreserve)
		
		vsizer.Add(hsizer)		
		vsizer.AddSpacer(10)
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(10)
		self.bThrowN = wx.Button(self, wx.ID_ANY, "Normal")
		hsizer.Add(self.bThrowN)
		self.Bind(wx.EVT_BUTTON, self.onBThrowN, self.bThrowN)
		self.bThrowN.Enable(False)
		self.bThrowN.SetToolTip("Throw turnout to NORMAL position")
		
		hsizer.AddSpacer(10)
		self.bThrowR = wx.Button(self, wx.ID_ANY, "Reverse")
		hsizer.Add(self.bThrowR)
		self.Bind(wx.EVT_BUTTON, self.onBThrowR, self.bThrowR)
		self.bThrowR.Enable(False)
		self.bThrowR.SetToolTip("Throw turnout to REVERSED position")
		
		hsizer.AddSpacer(10)
		self.bAngle = wx.Button(self, wx.ID_ANY, "Angle")
		hsizer.Add(self.bAngle)
		self.Bind(wx.EVT_BUTTON, self.onBAngle, self.bAngle)
		self.bAngle.Enable(False)
		self.bAngle.SetToolTip("Set servo to specific angle")
		
		vsizer.Add(hsizer)
		vsizer.AddSpacer(10)		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		
		hsizer.AddSpacer(10)
		self.bSwap = wx.Button(self, wx.ID_ANY, "Swap")
		hsizer.Add(self.bSwap)
		self.Bind(wx.EVT_BUTTON, self.onBSwap, self.bSwap)
		self.bSwap.Enable(False)
		self.bSwap.SetToolTip("Swap turnout NORMAL and REVERSE settings")
		
		hsizer.AddSpacer(10)
		self.bConfig = wx.Button(self, wx.ID_ANY, "Config")
		hsizer.Add(self.bConfig)
		self.Bind(wx.EVT_BUTTON, self.onBConfig, self.bConfig)
		self.bConfig.Enable(False)
		self.bConfig.SetToolTip("Reconfigure turnout/servo")
		
		hsizer.AddSpacer(30)
		self.bStore = wx.Button(self, wx.ID_ANY, "Store")
		hsizer.Add(self.bStore)
		self.Bind(wx.EVT_BUTTON, self.onBStore, self.bStore)
		self.bStore.SetToolTip("Store configuration")
		
		vsizer.Add(hsizer)		
		vsizer.AddSpacer(10)		
		
		hsizer = wx.BoxSizer(wx.HORIZONTAL)
		hsizer.AddSpacer(10)
		hsizer.Add(vsizer)
		hsizer.AddSpacer(10)
		
		self.SetSizer(hsizer)
		self.Layout()
		self.Fit()
		
	def onBSelectAll(self, _):
		self.lcServos.selectAll()
		
	def onBSelectNone(self, _):
		self.lcServos.selectNone()
		
	def onBThrowN(self, _):
		for tx in self.lcServos.getSelection():
			self.parent.throwTurnout(tx, True)
		self.update(self.parent.getServosMap())
		
	def onBThrowR(self, _):
		for tx in self.lcServos.getSelection():
			self.parent.throwTurnout(tx, False)
		self.update(self.parent.getServosMap())
		
	def onBAngle(self, _):
		dlg = AngleDlg(self)
		rc = dlg.ShowModal()
		
		if rc == wx.ID_OK:
			a = dlg.getValues()
			
		dlg.Destroy()
		if rc != wx.ID_OK:
			return 
		
		for sx in self.lcServos.getSelection():
			self.parent.setServoAngle(sx, a)
		self.update(self.parent.getServosMap())
		
	def onBSwap(self, _):
		for tx in self.lcServos.getSelection():
			self.parent.swapTurnout(tx)
		self.update(self.parent.getServosMap())
		
	def onBConfig(self, _):
		selection = self.lcServos.getSelection()
		tx = selection[0]
		toData = self.lcServos.getDataForTurnout(tx)
		
		dlg = ToConfigDlg(self, toData[0], toData[1], toData[2])
		rc = dlg.ShowModal()
		
		if rc == wx.ID_OK:
			n,r,i = dlg.getValues()
			
		dlg.Destroy()
		if rc != wx.ID_OK:
			return 
		
		for tx in selection:
			self.parent.setTurnoutLimits(tx, n, r, i)
		self.update(self.parent.getServosMap())
		
	def onBStore(self, _):
		self.parent.nodeStore()
		
	def enableButtons(self, ct):
		self.bThrowN.Enable(ct > 0)
		self.bThrowR.Enable(ct > 0)
		self.bAngle.Enable(ct > 0)
		self.bSwap.Enable(ct > 0)
		self.bConfig.Enable(ct > 0)
		
	def update(self, data):
		self.lcServos.update(data, self.cbPreserve.GetValue())
				
	def onClose(self, _):
		self.parent.dlgServosExit()
		self.Destroy()

