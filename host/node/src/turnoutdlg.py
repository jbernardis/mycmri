import wx

SCSIZE=(130, -1)

class TurnoutDlg(wx.Dialog):
    def __init__(self, parent, node, nservos):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Turnout Configuration")
        self.node = node
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        vsz = wx.BoxSizer(wx.VERTICAL)
        vsz.AddSpacer(10)

        h = wx.BoxSizer(wx.HORIZONTAL)
        h.Add(wx.StaticText(self, wx.ID_ANY, "Turnout number:"))
        h.AddSpacer(5)
        self.scTurnout = wx.SpinCtrl(self, wx.ID_ANY, "", size=SCSIZE)
        self.scTurnout.SetRange(0, nservos-1)
        self.scTurnout.SetValue(0)
        
        h.Add(self.scTurnout)
        h.AddSpacer(40)
                
        bRetrieve = wx.Button(self, wx.ID_ANY, "Retrieve")
        self.Bind(wx.EVT_BUTTON, self.onbRetrieve, bRetrieve)
        bRetrieve.SetToolTip("Retrieve Turnout Settings")
        h.Add(bRetrieve)
        h.AddSpacer(10)
        
        bSet = wx.Button(self, wx.ID_ANY, "Set")
        self.Bind(wx.EVT_BUTTON, self.onbSet, bSet)
        bSet.SetToolTip("Set Turnout Settings")
        h.Add(bSet)
        h.AddSpacer(20)
        
        bStore = wx.Button(self, wx.ID_ANY, "Store")
        self.Bind(wx.EVT_BUTTON, self.onbStore, bStore)
        bStore.SetToolTip("Store settings into EEPROM")
        h.Add(bStore)
        
        vsz.Add(h)
        vsz.AddSpacer(30)

        h = wx.BoxSizer(wx.HORIZONTAL)
        h.Add(wx.StaticText(self, wx.ID_ANY, "Normal Angle:"))
        h.AddSpacer(5)
        self.scNormal = wx.SpinCtrl(self, wx.ID_ANY, "", size=SCSIZE)
        self.scNormal.SetRange(0, 180)
        self.scNormal.SetValue(0)
        
        h.Add(self.scNormal)
        h.AddSpacer(20)
        
        h.Add(wx.StaticText(self, wx.ID_ANY, "Reverse Angle:"))
        h.AddSpacer(5)
        self.scReverse = wx.SpinCtrl(self, wx.ID_ANY, "", size=SCSIZE)
        self.scReverse.SetRange(0, 180)
        self.scReverse.SetValue(0)
        
        h.Add(self.scReverse)
        h.AddSpacer(20)
        
        h.Add(wx.StaticText(self, wx.ID_ANY, "Initial Angle:"))
        h.AddSpacer(5)
        self.scInitial = wx.SpinCtrl(self, wx.ID_ANY, "", size=SCSIZE)
        self.scInitial.SetRange(0, 180)
        self.scInitial.SetValue(0)
        
        h.Add(self.scInitial)
        h.AddSpacer(5)
        
        vsz.Add(h)
        vsz.AddSpacer(10)

 
        h = wx.BoxSizer(wx.HORIZONTAL)
        h.AddSpacer(20)
        
        bExit = wx.Button(self, wx.ID_ANY, "Exit")
        self.Bind(wx.EVT_BUTTON, self.onbExit, bExit)
        bExit.SetToolTip("Exit Dialog Box")
        h.Add(bExit)
        h.AddSpacer(20)
        
        vsz.Add(h)
        
        vsz.AddSpacer(10)
        sizer.AddSpacer(10)
        sizer.Add(vsz)
        sizer.AddSpacer(10)
        
        self.SetSizer(sizer)
        self.Fit()

    def onbRetrieve(self, _):
        tx = self.scTurnout.GetValue()
        self.node.getTurnoutLimits(tx)
        
    def insertRetrievedValues(self, norm, rev, ini):
        self.scNormal.SetValue(norm)
        self.scReverse.SetValue(rev)
        self.scInitial.SetValue(ini)

    def onbSet(self, _):
        tx = self.scTurnout.GetValue()
        norm = self.scNormal.GetValue()
        rev = self.scReverse.GetValue()
        ini = self.scInitial.GetValue()
        self.node.setTurnoutLimits(tx, norm, rev, ini)
        
    def onbStore(self, _):
        self.node.store()

    def onbExit(self, _):
        self.EndModal(wx.ID_OK)
