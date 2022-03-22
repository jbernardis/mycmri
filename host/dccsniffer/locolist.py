import wx

class LocoList(wx.ListCtrl):
	def __init__(self, parent):
		self.parent = parent
		
		wx.ListCtrl.__init__(
			self, parent, wx.ID_ANY, size=(240, 280),
			style=wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_VRULES|wx.LC_SINGLE_SEL
			)
		
		font = wx.Font(wx.Font(12, wx.FONTFAMILY_ROMAN, wx.NORMAL, wx.NORMAL, faceName="Arial"))
		self.SetFont(font)


		self.InsertColumn(0, "Loco")
		self.InsertColumn(1, "Speed")
		self.InsertColumn(2, "Dir")
		self.SetColumnWidth(0, 80)
		self.SetColumnWidth(1, 80)
		self.SetColumnWidth(2, 80)

		self.SetItemCount(0)
		self.locos = []

		self.normalA = wx.ItemAttr()
		self.normalB = wx.ItemAttr()
		self.normalA.SetBackgroundColour(wx.Colour(225, 255, 240))
		self.normalB.SetBackgroundColour(wx.Colour(138, 255, 197))
		
	def count(self):
		return len(self.locos)
	
	def updateLoco(self, loco, speed, direction):
		for tx in range(len(self.locos)):
			if self.locos[tx]["lid"] == loco:
				self.locos[tx]["speed"] = speed
				self.locos[tx]["direction"] = direction
				self.RefreshItem(tx)
				return
		self.locos.append({"lid": loco, "speed": speed, "direction": direction})
		self.SetItemCount(len(self.locos))

	def OnGetItemText(self, item, col):
		if item < 0 or item >= len(self.locos):
			return None
		
		tr = self.locos[item]
		if col == 0:
			return tr["lid"]
		elif col == 1:
			return "%3d" % tr["speed"]
		elif col == 2:
			return tr["direction"]

	def OnGetItemAttr(self, item):
		if item % 2 == 1:
			return self.normalB
		else:
			return self.normalA
