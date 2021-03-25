ON = 1
OFF = 0

nodeAddr = 0
actions = []
ep = None

inputs = []
flags = []
registers = []

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

	try:
		v = inputs[naddr][idx]
	except (KeyError, IndexError):
		return False
	
	return value == v

def Output(idx, value=True, nd=None):
	if nd is None:
		naddr = nodeAddr
	else:
		naddr = nd

	try:
		v = outputs[naddr][idx]
	except (KeyError, IndexError):
		return False
	
	return value == v

def Flag(idx, value=False, nd=None):
	if nd is None:
		naddr = nodeAddr
	else:
		naddr = nd

	try:
		v = flags[naddr][idx]
	except (KeyError, IndexError):
		return False
	
	return value == v

def Register(idx, value="", nd=None):
	if nd is None:
		naddr = nodeAddr
	else:
		naddr = nd

	try:
		v = registers[naddr][idx]
	except (KeyError, IndexError):
		return False
	
	return value == v

# output functions: setoutput, setflag, setregister, turnout/servo(normal, reverse, toggle, angle)
def SetOutput(idx, value=ON, nd=None):
	if nd is None:
		naddr = nodeAddr
	else:
		naddr = nd
		
	if value:
		actions.append(["outon", naddr, [idx]])
	else:
		actions.append(["outoff", naddr, [idx]])
		
def SetFlag(idx, value=True, nd=None):
	if nd is None:
		naddr = nodeAddr
	else:
		naddr = nd
		
	if value:
		actions.append(["flagon", naddr, [idx]])
	else:
		actions.append(["flagoff", naddr, [idx]])
		
def SetRegister(idx, value, nd=None):
	if nd is None:
		naddr = nodeAddr
	else:
		naddr = nd
		
	actions.append(["register", naddr, [idx, value]])

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
	
def initialize(i, o, f, r):
	global inputs
	global outputs
	global flags
	global registers
	global ep
	
	inputs = i
	outputs = o
	flags = f
	registers = r
	
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
