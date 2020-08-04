import wx
import glob
from node import Node
from nodeguidlg import NodeGuiDlg

class NodeProxy:
	def __init__(self, node):
		self.node = node
		self.gui = None
		self.inputsMap = []

class NodeTool(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, wx.ID_ANY, " NodeTool ", size=(500, 500))
		self.SetBackgroundColour(wx.Colour(255, 255, 255))
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.node = None
		self.nodeProxies = {}
		self.currentNode = None
		
		sz = wx.BoxSizer(wx.VERTICAL)
		sz.AddSpacer(20)
		
		l = wx.StaticText(self, wx.ID_ANY, "Port:")
		self.chPort = wx.Choice(self, wx.ID_ANY, choices = self.getTtyList())
		self.chPort.SetSelection(0)

		self.bRefresh = wx.Button(self, wx.ID_ANY, "Refresh")
		self.Bind(wx.EVT_BUTTON, self.onRefresh, self.bRefresh)
		
		self.bConnect = wx.Button(self, wx.ID_ANY, "Connect")
		self.Bind(wx.EVT_BUTTON, self.onConnect, self.bConnect)
		
		lhsz = wx.BoxSizer(wx.HORIZONTAL)
		lhsz.Add(l, 0, wx.TOP, 4)
		lhsz.AddSpacer(10)
		lhsz.Add(self.chPort)
		lhsz.AddSpacer(5)
		lhsz.Add(self.bRefresh)
		lhsz.AddSpacer(5)
		lhsz.Add(self.bConnect)
		sz.Add(lhsz)
		sz.AddSpacer(20)
		
		hsz = wx.BoxSizer(wx.HORIZONTAL)
		hsz.AddSpacer(20)
		hsz.Add(sz)
		hsz.AddSpacer(20)
		
		self.SetSizer(hsz)
		
		self.Layout()
		self.Fit()
		s = self.GetSize()
		s[1] += 50
		self.SetSize(s)

		self.Show()
		
	def getTtyList(self):
		return sorted(glob.glob("/dev/node*")) + sorted(glob.glob("/dev/ttyUSB*")) + sorted(glob.glob("/dev/ttyACM*"))
			
	def onTimer(self, _):
		self.currentNode.node.process()
		self.timerCt -= 1
		if self.timerCt < 0:
			self.timer.Stop()
			self.timer.Destroy()
			print("abandoning connect")
			self.bConnect.Enable(True)
			self.currentNode = None
			
	def identityRcvd(self, addr, inp, outp, servo):
		self.timer.Stop()
		self.timer.Destroy()
		if addr in self.nodeProxies:
			print("Address %d is already in use")
		else:
			self.currentNode.node.configure(addr, inp, outp, servo)
			self.currentNode.inputsMap = [True] * (inp*8)
			self.currentNode.node.registerCallback(None, None, None, None, None)
			self.currentNode.gui = NodeGuiDlg(self, self.currentNode.node)
			self.currentNode.gui.registerInputs(self.inputRcvd)
			self.nodeProxies[addr] = self.currentNode
		self.currentNode = None
		self.bConnect.Enable(True)
		
	def inputRcvd(self, addr, inp, val, delta):
		print("addr %d inp %d val %d delta %s" % (addr, inp, val, str(delta)))
		self.nodeProxies[addr].inputsMap[inp] = val
		if delta:
			print("take action based on input %d:%d changing to %d" % (addr, inp, val))
			if inp == 0 and val == 0:
				self.nodeProxies[addr].gui.setTurnout(31, True)
			elif inp == 1 and val == 0:
				self.nodeProxies[addr].gui.setTurnout(31, False)
			elif inp == 2 and val == 0:
				self.nodeProxies[addr].gui.setOutput(8, True)
			elif inp == 3 and val == 0:
				self.nodeProxies[addr].gui.setOutput(8, False)
			elif inp == 4 and val == 0:
				self.nodeProxies[addr].gui.setAngle(0, 90)
		
	def onRefresh(self, _):
		self.chPort.Clear()
		self.chPort.Set(self.getTtyList())
		self.chPort.SetSelection(0)

	def onConnect(self, _):
		px = self.chPort.GetSelection()
		p = self.chPort.GetString(px)
		for np in self.nodeProxies:
			if self.nodeProxies[np].node.tty == p:
				print("Port is already in use: %s" % p)
				return
		
		self.bConnect.Enable(False)
		node = Node()
		node.registerCallback(None, self.identityRcvd, None, None, None)
		node.connect(p, 115200)
		node.getIdentity()
		node.start(poll=False)
		self.currentNode = NodeProxy(node)
		
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.onTimer, self.timer)
		self.timerCt = 60
		self.timer.Start(250)
		
	def nodeDlgClose(self, p):
		try:
			del(self.nodeProxies[p])
		except:
			False
						
	def onClose(self, _):
		for p in self.nodeProxies:
			try:
				self.nodeProxies[p].gui.Destroy()
			except:
				pass

			node = self.nodeProxies[p].node	
			try:
				node.stop()
				node.disconnect()
			except:
				pass

		self.Destroy()

if __name__ == '__main__':
	app = wx.App()
	frame = NodeTool()
	frame.Show(True)
	app.MainLoop()
