import wx

SCSIZE=(130, -1)

class ServoAngleDlg(wx.Dialog):
    def __init__(self, parent, node, nservos):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Set Servo Angle")
        self.node = node
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        vsz = wx.BoxSizer(wx.VERTICAL)
        vsz.AddSpacer(10)

        h = wx.BoxSizer(wx.HORIZONTAL)
        h.Add(wx.StaticText(self, wx.ID_ANY, "Servo number:"))
        h.AddSpacer(5)
        self.scServo = wx.SpinCtrl(self, wx.ID_ANY, "", size=SCSIZE)
        self.scServo.SetRange(0, nservos-1)
        self.scServo.SetValue(0)
        
        h.Add(self.scServo)
        h.AddSpacer(40)
        
        h.Add(wx.StaticText(self, wx.ID_ANY, "Angle:"))
        h.AddSpacer(5)
        self.scAngle = wx.SpinCtrl(self, wx.ID_ANY, "", size=SCSIZE)
        self.scAngle.SetRange(0, 180)
        self.scAngle.SetValue(0)
        
        h.Add(self.scAngle)
        h.AddSpacer(20)
        
        bSet = wx.Button(self, wx.ID_ANY, "Set")
        self.Bind(wx.EVT_BUTTON, self.onbSet, bSet)
        bSet.SetToolTip("Set Servo Settings")
        h.Add(bSet)
        h.AddSpacer(20)
        
        vsz.Add(h)
        vsz.AddSpacer(10)

        h = wx.BoxSizer(wx.HORIZONTAL)
        h.AddSpacer(20)
        bExit = wx.Button(self, wx.ID_ANY, "Exit")
        self.Bind(wx.EVT_BUTTON, self.onbExit, bExit)
        bExit.SetToolTip("Exit Dialog Box")
        h.Add(bExit)
        
        vsz.Add(h)
        
        vsz.AddSpacer(10)
        sizer.AddSpacer(10)
        sizer.Add(vsz)
        sizer.AddSpacer(10)
        
        self.SetSizer(sizer)
        self.Fit()

    def onbSet(self, _):
        sx = self.scServo.GetValue()
        angle = self.scAngle.GetValue()
        self.node.setAngle(sx, angle)

    def onbExit(self, _):
        self.EndModal(wx.ID_OK)
