import wx
from wx.lib import newevent
from serial import SerialException

from dccsniffer import SnifferThread
from locolist import LocoList


(DCCMessageEvent, EVT_DCCMESSAGE) = newevent.NewEvent()  
(DCCClosedEvent,  EVT_DCCCLOSED)  = newevent.NewEvent()  

class MyFrame(wx.Frame):

	def __init__(self):
		wx.Frame.__init__(self, None, -1, "My Frame", size=(300, 300))
		self.Bind(wx.EVT_CLOSE, self.onClose)
		
		self.sniffer = None
		
		sz = wx.BoxSizer(wx.VERTICAL)
		sz.AddSpacer(20)
		
		st = wx.StaticText(self, -1, "Sniffer Tester")
		nbFont = wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
		st.SetForegroundColour(wx.Colour(37, 61, 180))
		st.SetFont(nbFont)
		
		sz.Add(st)
		
		sz.AddSpacer(20)
		
		self.locolist = LocoList(self)
		sz.Add(self.locolist)
		sz.AddSpacer(20)
		
		bsz = wx.BoxSizer(wx.HORIZONTAL)
		bsz.AddSpacer(20)
		
		self.bConnect = wx.Button(self, wx.ID_ANY, "Connect")
		bsz.Add(self.bConnect)
		self.Bind(wx.EVT_BUTTON, self.onConnectPressed, self.bConnect)

		
		bsz.AddSpacer(10)
		
		self.bDisconnect = wx.Button(self, wx.ID_ANY, "Disconnect")
		bsz.Add(self.bDisconnect)
		self.Bind(wx.EVT_BUTTON, self.onDisconnectPressed, self.bDisconnect)
		
		bsz.AddSpacer(20)
		
		sz.Add(bsz)
		sz.AddSpacer(20)
		
		self.SetSizer(sz)
		self.Layout()
		self.Fit()
		
		self.Bind(EVT_DCCMESSAGE, self.onDCCMessage)
		self.Bind(EVT_DCCCLOSED,  self.onDCCClosed)
		
		self.Show()
		
	def onConnectPressed(self, _):
		self.connectSniffer()

	def connectSniffer(self):		
		self.sniffer = SnifferThread()
		self.sniffer.bind(self.DCCMessage, self.DCCClosed)

		port = "/dev/ttyACM0"
		try:
			self.sniffer.connect(port, 38400, 1)
		except SerialException:
			print("Unable to open port %s" % port)
			self.sniffer = None

		if self.sniffer:
			self.sniffer.start()
		
	def onDisconnectPressed(self, _):
		self.disconnectSniffer()
		
	def disconnectSniffer(self):
		try:
			self.sniffer.kill()
			self.sniffer.join()	
		except:
			pass
		
		self.sniffer = None
			
	def DCCMessage(self, txt): # thread context
		dccMsg = {
			"instr": txt[0],
			"loco": txt[1],
			"param": txt[2]
		}
		evt = DCCMessageEvent(dcc=dccMsg)
		wx.PostEvent(self, evt)
		
	def onDCCMessage(self, evt):
		print("Message: %s" % str(evt.dcc))
		dccMsg = evt.dcc
		print(str(dccMsg))
		cmd = dccMsg["instr"]
		if cmd in ["F", "f", "R", "r", "s", "e"]:
			if cmd in ["F", "f"]:
				direction = "Forward"
			elif cmd in ["R", "r"]:
				direction = "Reverse"
			else:
				direction = "Stopped"
			speed = int(dccMsg["param"])
			self.locolist.updateLoco(dccMsg["loco"], speed, direction)
		
	def DCCClosed(self): # thread context
		evt = DCCClosedEvent()
		wx.PostEvent(self, evt)
		
	def onDCCClosed(self, evt):
		print("Thread terminated event")
		self.disconnectSniffer()
		
	def onClose(self, evt):
		self.disconnectSniffer()
		self.Destroy()

class App(wx.App):
	def OnInit(self):
		self.frame = MyFrame()
		self.frame.Show()
		self.SetTopWindow(self.frame)
		return True

app = App(False)
app.MainLoop()
