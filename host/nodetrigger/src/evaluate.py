ON = 1
OFF = 0

nodeAddr = 0
actions = []
RR = None
ep = None

# set node address default value
def Node(n):
	global nodeAddr
	nodeAddr = n

# testing functions:  input, output, flag, register	
def Input(idx, value=False, nd=None):
	if nd is None:
		naddr = nodeAddr
	else:
		naddr = nd
	print("look for input %d at address %d" % (idx, naddr))

	v = RR.getInput(naddr, idx)	
	print("got back (%s)" % v)
	return value == v

def Output(idx, value=True, nd=None):
	if nd is None:
		naddr = nodeAddr
	else:
		naddr = nd
	print("look for output %d at address %d" % (idx, naddr))

	v = RR.getOutput(naddr, idx)
	print("got back (%s)" % v)
	return value == v

# output functions: setoutput, pulseOutput, setflag, setregister, turnout/servo(normal, reverse, toggle, angle)
def SetOutput(idx, value=ON, nd=None):
	if nd is None:
		naddr = nodeAddr
	else:
		naddr = nd
		
	if value:
		actions.append(["outon", naddr, [idx]])
	else:
		actions.append(["outoff", naddr, [idx]])
		
def PulseOutput(idx, length=1, nd=None):
	if nd is None:
		naddr = nodeAddr
	else:
		naddr = nd
		
	actions.append(["pulse", naddr, [idx, length]])
		
def Normal(idx, nd=None):
	if nd is None:
		naddr = nodeAddr
	else:
		naddr = nd
		
	actions.append(["normal", naddr, [idx]])

def Reverse(idx, nd=None):
	if nd is None:
		naddr = nodeAddr
	else:
		naddr = nd
		
	actions.append(["reverse", naddr, [idx]])
	
def Toggle(idx, nd=None):
	if nd is None:
		naddr = nodeAddr
	else:
		naddr = nd
		
	actions.append(["toggle", naddr, [idx]])
	
def Angle(idx, angle, nd=None):
	if nd is None:
		naddr = nodeAddr
	else:
		naddr = nd
		
	actions.append(["angle", naddr, [idx, angle]])
	
def initialize(rr):
	global RR
	global ep
	
	RR = rr
	
	fn = "rules.pyr"
	try:
		with open(fn, "rb") as source_file:
			code = compile(source_file.read(), fn, "exec")
	except FileNotFoundError:
		print("Unable to find \'%s\' file" % fn)
		exit(1)
		
	exec(code, globals())

	try:
		ep = globals()["rules"]	
	except KeyError:
		print("invalid rules.py file.  Cannot find \'rules\' entry point")
		exit(1)	

def evaluate():
	global actions
	
	actions = []
	ep()
	return actions
